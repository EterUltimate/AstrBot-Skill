from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class EventHookInfo:
    register_function: str
    decorator: str
    event_type: str | None
    doc: str
    required_params: list[str]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_ast(path: Path) -> ast.AST:
    return ast.parse(_read_text(path), filename=str(path))


def _extract_event_types(star_handler_py: Path) -> dict[str, str]:
    """Extract EventType enum members -> comment/description."""
    text = _read_text(star_handler_py)
    in_enum = False
    event_types: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("class EventType"):
            in_enum = True
            continue
        if in_enum:
            if line.startswith("class ") or line.startswith("@dataclass") or line.startswith("H ="):
                break
            if "= enum.auto()" in line:
                # Example: OnLLMRequestEvent = enum.auto()  # comment
                left, _, right = line.partition("=")
                name = left.strip()
                comment = ""
                if "#" in right:
                    comment = right.split("#", 1)[1].strip()
                event_types[name] = comment
    return event_types


def _extract_required_params(doc: str) -> list[str]:
    """Heuristic parsing for lines like: 请务必接收三个参数：event, tool, tool_args"""
    for line in doc.splitlines():
        line = line.strip()
        if not line.startswith("请务必接收"):
            continue
        if "参数" not in line or "：" not in line:
            continue
        _, _, tail = line.partition("：")
        parts = [p.strip() for p in tail.split(",") if p.strip()]
        return parts
    return []


def _decorator_name_from_register(register_fn: str) -> str:
    # register_on_llm_request -> on_llm_request
    # register_after_message_sent -> after_message_sent
    suffix = register_fn
    if suffix.startswith("register_"):
        suffix = suffix[len("register_") :]
    return f"@filter.{suffix}()"


def _guess_event_type(register_fn: str) -> str | None:
    mapping = {
        "register_on_astrbot_loaded": "OnAstrBotLoadedEvent",
        "register_on_platform_loaded": "OnPlatformLoadedEvent",
        "register_on_waiting_llm_request": "OnWaitingLLMRequestEvent",
        "register_on_llm_request": "OnLLMRequestEvent",
        "register_on_llm_response": "OnLLMResponseEvent",
        "register_on_decorating_result": "OnDecoratingResultEvent",
        "register_after_message_sent": "OnAfterMessageSentEvent",
        "register_on_using_llm_tool": "OnUsingLLMToolEvent",
        "register_on_llm_tool_respond": "OnLLMToolRespondEvent",
    }
    return mapping.get(register_fn)


def _extract_event_hooks(register_py: Path) -> list[EventHookInfo]:
    tree = _parse_ast(register_py)
    hooks: list[EventHookInfo] = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if not node.name.startswith("register_"):
            continue
        if node.name in {"register_llm_tool", "register_agent"}:
            continue
        if not (node.name.startswith("register_on_") or node.name.startswith("register_after_")):
            continue
        doc = ast.get_docstring(node) or ""
        required_params = _extract_required_params(doc)
        if node.name == "register_on_llm_response" and required_params == [
            "event",
            "request",
        ]:
            # The core docstring currently says "event, request", but the actual
            # handler signature uses (event, response).
            required_params = ["event", "response"]

        hooks.append(
            EventHookInfo(
                register_function=node.name,
                decorator=_decorator_name_from_register(node.name),
                event_type=_guess_event_type(node.name),
                doc=doc.strip(),
                required_params=required_params,
            )
        )
    hooks.sort(key=lambda h: h.register_function)
    return hooks


def _extract_agent_run_hooks(agent_hooks_py: Path) -> dict[str, Any]:
    tree = _parse_ast(agent_hooks_py)
    base_cls: ast.ClassDef | None = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "BaseAgentRunHooks":
            base_cls = node
            break
    if base_cls is None:
        return {"error": "BaseAgentRunHooks not found"}

    methods: list[dict[str, Any]] = []
    for node in base_cls.body:
        if not isinstance(node, ast.AsyncFunctionDef):
            continue
        arg_names = [a.arg for a in node.args.args]
        methods.append(
            {
                "name": node.name,
                "args": arg_names,
                "doc": (ast.get_docstring(node) or "").strip(),
            }
        )

    return {
        "interface": "BaseAgentRunHooks",
        "methods": methods,
        "typical_order": [
            "on_agent_begin",
            "on_tool_start",
            "on_tool_end",
            "on_agent_done",
        ],
        "call_sites": [
            "astrbotcore/astrbot/core/agent/runners/tool_loop_agent_runner.py",
            "astrbotcore/astrbot/core/agent/runners/dashscope/dashscope_agent_runner.py",
            "astrbotcore/astrbot/core/agent/runners/dify/dify_agent_runner.py",
            "astrbotcore/astrbot/core/agent/runners/coze/coze_agent_runner.py",
        ],
    }


def main() -> int:
    root = _repo_root()
    out_dir = root / "docs" / ".tmp" / "hook_inventory"
    out_dir.mkdir(parents=True, exist_ok=True)

    register_py = root / "astrbotcore" / "astrbot" / "core" / "star" / "register" / "star_handler.py"
    star_handler_py = root / "astrbotcore" / "astrbot" / "core" / "star" / "star_handler.py"
    agent_hooks_py = root / "astrbotcore" / "astrbot" / "core" / "agent" / "hooks.py"

    event_types = _extract_event_types(star_handler_py)
    event_hooks = _extract_event_hooks(register_py)
    agent_hooks = _extract_agent_run_hooks(agent_hooks_py)

    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "event_types": str(star_handler_py.relative_to(root)).replace("\\", "/"),
            "event_hooks_register": str(register_py.relative_to(root)).replace("\\", "/"),
            "agent_hooks_interface": str(agent_hooks_py.relative_to(root)).replace("\\", "/"),
        },
        "event_types": event_types,
        "event_hooks": [hook.__dict__ for hook in event_hooks],
        "agent_run_hooks": agent_hooks,
    }

    (out_dir / "hooks.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    md_lines: list[str] = []
    md_lines.append("# Hook Inventory (Generated)")
    md_lines.append("")
    md_lines.append(f"- Generated at (UTC): `{payload['generated_at']}`")
    md_lines.append("")
    md_lines.append("## Event Hooks (`@filter.on_*`)")
    md_lines.append("")
    for h in event_hooks:
        tip = f" ({h.event_type})" if h.event_type else ""
        md_lines.append(f"- `{h.decorator}`{tip}")
        if h.required_params:
            md_lines.append(f"  - required params: `{', '.join(h.required_params)}`")
    md_lines.append("")
    md_lines.append("## Agent Run Hooks (`BaseAgentRunHooks`)")
    md_lines.append("")
    md_lines.append(f"- interface: `{agent_hooks.get('interface', '')}`")
    md_lines.append(f"- typical order: `{', '.join(agent_hooks.get('typical_order', []))}`")
    md_lines.append("")
    for m in agent_hooks.get("methods", []):
        md_lines.append(f"- `{m.get('name')}` args: `{', '.join(m.get('args', []))}`")

    (out_dir / "hooks.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"Wrote: {out_dir / 'hooks.json'}")
    print(f"Wrote: {out_dir / 'hooks.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
