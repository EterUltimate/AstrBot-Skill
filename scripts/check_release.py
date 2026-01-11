import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple
from urllib.request import Request, urlopen


SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$")


def _parse_semver(tag: str) -> Optional[Tuple[int, int, int]]:
    m = SEMVER_RE.match((tag or "").strip())
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def _pick_latest_semver(tags: List[str]) -> Optional[str]:
    best_tag = None
    best_ver = None
    for tag in tags:
        ver = _parse_semver(tag)
        if not ver:
            continue
        if best_ver is None or ver > best_ver:
            best_ver = ver
            best_tag = tag
    return best_tag


def _http_get_json(url: str, token: str = "") -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "AstrBot-docs-release-bot",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)


def _write_github_output(kv: Dict[str, str]) -> None:
    out_path = os.getenv("GITHUB_OUTPUT")
    if not out_path:
        for k, v in kv.items():
            print(f"{k}={v}")
        return
    with open(out_path, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def main() -> int:
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not repo:
        print("GITHUB_REPOSITORY is required.", file=sys.stderr)
        return 2

    upstream_repo = os.getenv("UPSTREAM_REPO", "AstrBotDevs/AstrBot").strip()

    upstream_tags = _http_get_json(
        f"https://api.github.com/repos/{upstream_repo}/tags?per_page=100"
    )
    upstream_tag = _pick_latest_semver([t.get("name", "") for t in (upstream_tags or [])])
    if not upstream_tag:
        print("No semver-like tag found in upstream tags.", file=sys.stderr)
        return 3

    releases = _http_get_json(
        f"https://api.github.com/repos/{repo}/releases?per_page=100", token=token
    )
    current_tag = _pick_latest_semver([r.get("tag_name", "") for r in (releases or [])]) or ""

    should_release = False
    reason = ""
    if not current_tag:
        should_release = True
        reason = "no existing releases"
    else:
        upstream_ver = _parse_semver(upstream_tag)
        current_ver = _parse_semver(current_tag)
        if upstream_ver and current_ver and upstream_ver > current_ver:
            should_release = True
            reason = f"upstream {upstream_tag} newer than {current_tag}"
        else:
            should_release = False
            reason = f"upstream {upstream_tag} not newer than {current_tag}"

    release_title = f"更新到 AstrBot {upstream_tag} 版本的文档"
    release_body = f"更新到 AstrBot {upstream_tag} 版本的文档。附件仅包含仓库 docs/ 目录内容的压缩包。"
    asset_name = f"docs-{upstream_tag}.zip"

    _write_github_output(
        {
            "upstream_tag": upstream_tag,
            "current_tag": current_tag,
            "should_release": "true" if should_release else "false",
            "reason": reason,
            "release_title": release_title,
            "release_body": release_body,
            "asset_name": asset_name,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
