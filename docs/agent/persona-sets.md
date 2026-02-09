---
category: agent
---

# Persona（人格）管理

Persona（人格）用于定义：

- 系统提示词（System Prompt）
- 预设对话（Begin Dialogs）
- 关联工具（Tools）

Persona 会参与构建 Agent/LLM 请求，是“让同一套模型表现出不同角色/能力边界”的主要机制之一。

## PersonaManager 常用操作

- `context.persona_manager.get_persona(persona_id)`：获取人格
- `context.persona_manager.get_all_personas()`：列出所有人格
- `context.persona_manager.create_persona(persona_id, system_prompt, begin_dialogs=None, tools=None)`：创建人格
- `context.persona_manager.update_persona(persona_id, system_prompt=None, begin_dialogs=None, tools=None)`：更新人格
- `context.persona_manager.delete_persona(persona_id)`：删除人格

## 与对话分支的关系

Persona 可以绑定在“对话分支（Conversation）”上，也可以来自会话级配置或全局默认；具体优先级与“显式禁用机制”见：

- `docs/agent/persona-resolution.md`

## 配置集成（WebUI 下拉选择）

在插件配置 Schema 中，可以使用 `_special: "select_persona"` 让用户从 WebUI 下拉选择已配置的人格。

## 相关源码位置

- PersonaManager：`astrbotcore/astrbot/core/persona_mgr.py`
- Persona 选择/注入逻辑（与对话/会话联动）：`astrbotcore/astrbot/core/provider/manager.py`、`astrbotcore/astrbot/core/conversation_mgr.py`
