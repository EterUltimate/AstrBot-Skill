---
category: agent
---

# Tools（函数调用 / Function Calling）

AstrBot 的工具体系主要有两种使用方式：

1) **插件事件侧的函数工具**：`@filter.llm_tool(...)`（用 docstring 生成 schema）  
2) **Agent/工具循环侧的工具对象**：`FunctionTool` + `ToolSet`（更适合复杂工具、子智能体、沙盒）

两者最终都会进入“模型可调用工具”的集合，并会触发对应的事件钩子（见 `docs/plugin_config/hooks.md`）。

## 方式 A：`@filter.llm_tool`（快速）

适合：简单逻辑、参数少、直接把结果交给模型总结。

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.llm_tool(name="get_weather")
async def get_weather(self, event: AstrMessageEvent, location: str):
    """获取天气信息。

    Args:
        location(string): 地点
    """
    return f"{location} 的天气是……"
```

要点：

- AstrBot 会解析 **docstring** 生成 tool schema（参数类型必须写在 `Args:` 里）。
- 返回 `str`：会被注入到下一轮 LLM 上下文；返回 `None`：不会注入。
- 需要“发消息/终止事件传播”时可以用 `yield` 配合 `event.stop_event()`（但请谨慎）。

## 方式 B：`FunctionTool`（推荐用于 Agent/复杂工具）

适合：复杂参数、需要强类型、需要复用/组合、需要和 Agent runner 深度集成（例如 handoff 子智能体）。

```python
from dataclasses import dataclass, field
from astrbot.api.all import FunctionTool, AstrAgentContext, ToolExecResult, ContextWrapper

@dataclass
class MyTool(FunctionTool[AstrAgentContext]):
    name: str = "tool_name"
    description: str = "工具描述"
    parameters: dict = field(default_factory=lambda: {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"}
        },
        "required": ["query"],
    })

    async def call(self, context: ContextWrapper[AstrAgentContext], **kwargs) -> ToolExecResult:
        return "tool result"
```

注册方式（常见）：

- 在插件 `__init__` 中：`self.context.add_llm_tools(MyTool())`
- 在工具循环 Agent 调用时传入：`tools=ToolSet([MyTool()])`

## 工具调用相关 Hooks（强烈建议知道）

工具调用时可以用事件钩子做审计/装饰（不要用它做权限硬隔离）：

- `@filter.on_using_llm_tool()`：工具调用前
- `@filter.on_llm_tool_respond()`：工具调用后

详见：`docs/plugin_config/hooks.md`

## 运行时“官方工具”注入（主 Agent）

主 Agent 在构建时会按配置注入一部分内置工具：

- Sandbox / computer-use：执行 shell、运行 Python、文件上传/下载（见 `docs/agent/sandbox.md`）
- Cron：创建/删除/列出定时任务（见 `docs/agent/cron.md`）

注入逻辑入口：

- `astrbotcore/astrbot/core/astr_main_agent.py`

## 相关源码位置

- `@filter.llm_tool` 解析与注册：`astrbotcore/astrbot/core/star/register/star_handler.py`（`register_llm_tool`）
- 工具对象与执行：`astrbotcore/astrbot/core/agent/tool.py`、`astrbotcore/astrbot/core/agent/tool_executor.py`
- Agent runner（工具循环）：`astrbotcore/astrbot/core/agent/runners/tool_loop_agent_runner.py`
