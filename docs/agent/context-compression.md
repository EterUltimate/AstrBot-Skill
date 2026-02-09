---
category: agent
---

# 上下文控制与压缩（Context Compression）

Agent 运行时经常会遇到“上下文长度超限”。AstrBot 提供了两类策略：

- **按轮次截断**：丢弃更早的对话轮次
- **LLM 摘要压缩**：用另一个模型把旧上下文总结成更短的摘要（再继续对话）

核心目标：在不无限增长 token 的前提下，保持可用的短期记忆与任务连续性。

## `ContextManager`（核心入口）

- `astrbotcore/astrbot/core/agent/context/manager.py`

它会基于 `ContextConfig` 执行：

1) enforce max turns（按轮次强制保留最近 N 轮）  
2) token-based compression（超过 token 限制时触发压缩/截断）

相关配置结构：

- `astrbotcore/astrbot/core/agent/context/config.py`

## 常见配置项（概念层）

- `max_context_tokens`：上下文 token 上限（<=0 表示不限制）
- `enforce_max_turns`：最多保留多少轮（-1 表示不限制）
- `truncate_turns`：触发截断时一次丢弃多少轮
- `llm_compress_provider`：摘要压缩用的 provider（为空则退回到截断策略）
- `llm_compress_keep_recent`：压缩时保留最近多少条消息不被总结
- `llm_compress_instruction`：摘要压缩指令（决定摘要格式与保真度）

## 与主 Agent 配置的关系

主 Agent 构建阶段会根据配置决定是否启用 “llm_compress” 以及选择哪一个 provider 来做压缩。

实现入口：

- `astrbotcore/astrbot/core/astr_main_agent.py`

常见配置键名（名称对齐）：

- `provider_settings.context_limit_reached_strategy`: `truncate_by_turns` / `llm_compress`
- `provider_settings.llm_compress_instruction`
- `provider_settings.llm_compress_keep_recent`
- `provider_settings.llm_compress_provider_id`
- `provider_settings.max_context_length`（按轮次控制）

默认配置入口：

- `astrbotcore/astrbot/core/config/default.py`

## 调试建议

- 如果你看到“突然忘记早期信息”：先确认是否触发了截断或摘要压缩
- 如果摘要质量差：单独为压缩选择更稳的 provider（不要和主对话模型共用）
- 如果工具循环经常跑偏：限制 `max_steps`，并将压缩指令写得更结构化（例如保留事实表、待办表）
