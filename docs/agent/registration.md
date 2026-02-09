---
category: agent
---

# Agent 注册（高级）

AstrBot 的“Agent”既可以通过配置（例如 subagent orchestrator）加载，也可以通过更底层的注册接口把 Agent 以 handoff tool 的形式暴露给模型。

> 注意：`register_agent` 属于 core 注册层能力，默认不在 `astrbot.api.event.filter` 中导出。  
> 更推荐优先使用配置式子智能体（见 `docs/agent/subagents.md`）。

## `register_agent`（core 注册层）

定义位置：

- `astrbotcore/astrbot/core/star/register/star_handler.py`（`register_agent`）

它会：

1) 构造一个 `Agent` 对象（name/instructions/tools/run_hooks）
2) 创建一个 `HandoffTool(agent=...)`
3) 把 handoff tool 放入全局工具列表，供主模型选择调用

相关实现：

- Agent 数据结构：`astrbotcore/astrbot/core/agent/agent.py`
- HandoffTool：`astrbotcore/astrbot/core/agent/handoff.py`

## `run_hooks`（Agent 运行钩子）

`register_agent(..., run_hooks=...)` 允许为该 Agent 绑定 `BaseAgentRunHooks`：

- 接口：`astrbotcore/astrbot/core/agent/hooks.py`
- 行为说明：`docs/agent/hooks.md`

## 什么时候需要用它

- 你要提供“可复用的专业子智能体”，并希望主 Agent 通过 handoff 调度它
- 你需要为某个 Agent 绑定特殊的 run hooks（审计、工具装饰、结果后处理）

如果你的需求只是“让模型会调用工具”，优先用：

- `FunctionTool` + `ToolSet`（`docs/agent/tools.md`）
- 配置式 subagent orchestrator（`docs/agent/subagents.md`）
