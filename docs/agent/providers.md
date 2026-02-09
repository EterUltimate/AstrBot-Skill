---
category: agent
---

# Providers（LLM / VLM / Embedding / STT / TTS）

在 Agent 体系里，“模型能力”统一由 Provider 管理。LLM/VLM/Embedding/STT/TTS 都属于 Provider 的不同类型，你在写插件/Agent 时通常只需要从 `context` 获取当前会话正在使用的 provider。

## 常用获取方式（Context 方法）

- `context.get_using_provider(umo: str) -> Provider | None`：获取当前会话正在使用的对话模型（Chat Completion）。
- `context.get_provider_by_id(provider_id: str)`：按 id 获取指定 provider。
- `context.get_all_providers()`：列出所有已配置的对话模型 provider。
- `context.get_using_stt_provider(umo: str)` / `context.get_using_tts_provider(umo: str)`：获取当前使用的 STT/TTS provider。
- `context.get_all_embedding_providers()`：列出所有 embedding provider（常用于知识库/检索）。

> 这些方法的真实实现入口：`astrbotcore/astrbot/core/star/context.py`  
> provider 的装配与会话隔离逻辑：`astrbotcore/astrbot/core/provider/manager.py`

## Provider 类型（概念对齐）

- Chat（LLM/VLM）：用于对话与工具循环（`tool_loop_agent` 的 `chat_provider_id` 指向这里）
- Embedding：用于向量化（知识库检索、相似度搜索）
- STT：语音转文本（Speech-to-Text）
- TTS：文本转语音（Text-to-Speech）

是否“支持 VLM（图像输入）”取决于具体 provider 的能力与配置；当 provider 不支持某些模态时，部分运行时会做清理/降级（参考：`astrbotcore/astrbot/core/astr_main_agent.py` 的配置项与处理逻辑）。

## 与 Agent 的关系

- Agent 的主入口通常需要一个对话 provider：`chat_provider_id`
- 工具调用/子智能体 handoff/沙盒工具注入都围绕这个对话 provider 驱动
- 如果你在同一条会话里需要“不同 provider（例如子智能体用不同模型）”，可参考 `docs/agent/subagents.md`（handoff tool 支持 per-subagent provider override）

## 相关源码位置（快速定位）

- ProviderManager：`astrbotcore/astrbot/core/provider/manager.py`
- Provider 类型定义：`astrbotcore/astrbot/core/provider/entities.py`
- Context 对外方法：`astrbotcore/astrbot/core/star/context.py`
