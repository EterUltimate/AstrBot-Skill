---
category: agent
---

# Sandbox（Computer Use Runtime）

AstrBot 的 Agent 运行时可以按配置注入“计算机使用”相关工具（例如执行 shell、运行 Python、上传/下载文件），并支持将运行环境切到沙盒。

## 关键概念

- `computer_use_runtime`：运行时类型（通常是 `none` / `local` / `sandbox`）
- sandbox booter：沙盒启动器（目前核心实现以 Shipyard 为主）
- sandbox tools：执行/文件工具，会被注入到主 Agent 的 `ToolSet`

## 运行时行为（高层）

- 当 `computer_use_runtime == "sandbox"` 时，主 Agent 构建阶段会注入沙盒工具，并在 system prompt 中追加 sandbox 模式说明。
- Shipyard 配置不完整时会直接跳过注入（避免误导模型）。

## 配置位置（以代码为准）

主 Agent 构建与注入逻辑：

- `astrbotcore/astrbot/core/astr_main_agent.py`

沙盒 client 与启动器：

- `astrbotcore/astrbot/core/computer/computer_client.py`
- `astrbotcore/astrbot/core/computer/booters/shipyard.py`
- `astrbotcore/astrbot/core/computer/booters/boxlite.py`

工具实现（示例）：

- `astrbotcore/astrbot/core/computer/tools/`

## 常见配置键（名称对齐）

以下是常见的配置键名（具体结构以你的配置文件与默认配置为准）：

- `provider_settings.computer_use_runtime`: `none` / `local` / `sandbox`
- `provider_settings.sandbox.booter`: 通常为 `shipyard`
- `provider_settings.sandbox.shipyard_endpoint`
- `provider_settings.sandbox.shipyard_access_token`
- `provider_settings.sandbox.shipyard_ttl`
- `provider_settings.sandbox.shipyard_max_sessions`

默认配置入口：

- `astrbotcore/astrbot/core/config/default.py`

## 常见注意事项

- 不要把 sandbox 当成“权限系统”：它只是降低风险的运行环境。真正的权限/安全边界应当在工具实现层做硬限制。
- 当模型产出文件路径（图片/音频/文件）时，路径可能来自本地或沙盒；某些资源组件会尝试从沙盒下载到本地再发送（参考：`astrbotcore/astrbot/core/astr_main_agent_resources.py`）。
