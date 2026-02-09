---
category: agent
---

# Subagents（子智能体 / Handoff）

AstrBot 支持把“子智能体”以 **handoff tool** 的形式注册到主 Agent 的工具集中，使主 Agent 可以通过工具调用把任务转交给某个子智能体执行。

子智能体通常由配置加载（更稳定、可运维），也可以通过更底层的注册接口拼装（更灵活但更偏内部）。

## 配置式子智能体（推荐）

核心机制：`SubAgentOrchestrator` 从配置加载子智能体定义，并注册对应的 handoff 工具（默认命名：`transfer_to_<agent_name>`）。

实现入口：

- `astrbotcore/astrbot/core/subagent_orchestrator.py`
- handoff 工具：`astrbotcore/astrbot/core/agent/handoff.py`

配置键名（名称对齐）：

- `subagent_orchestrator.agents`: 子智能体列表

### 配置字段（以代码为准）

每个 agent item 常见字段：

- `enabled`：是否启用
- `name`：子智能体名称（会进入 handoff tool 名称）
- `persona_id`：可选，引用 Persona（system_prompt / begin_dialogs / tools）
- `system_prompt`：没有 persona 时使用的指令
- `public_description`：给主 LLM 看的简短描述（影响它是否选择调用该 subagent）
- `provider_id`：可选，为该 subagent 指定对话 provider（覆盖默认 provider）
- `tools`：工具列表（字符串 id 列表）

### 行为要点

- 如果设置了 `persona_id`，会优先使用 persona 的 system_prompt、begin_dialogs 与 tools（并对 `public_description` 做 fallback）。
- `provider_id` 允许为某个 subagent 指定更合适/更便宜的模型。

## 调试与排障

如果主 Agent 从不调用某个子智能体，优先检查：

- `public_description` 是否足够清晰、短、可行动（主 LLM 只能看到这一段）
- 子智能体 `name` 是否合理（会影响工具名 `transfer_to_<name>`）
- 主 Agent 的工具集合里是否确实包含该 handoff tool（看注册日志/或直接在运行时打印工具列表）

## 相关源码位置

- SubAgentOrchestrator：`astrbotcore/astrbot/core/subagent_orchestrator.py`
- HandoffTool：`astrbotcore/astrbot/core/agent/handoff.py`
- Agent 数据结构：`astrbotcore/astrbot/core/agent/agent.py`
