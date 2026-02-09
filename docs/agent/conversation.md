---
category: agent
---

# 会话与对话分支（Conversation）

AstrBot 把“会话（Session）”与“对话分支（Conversation）”分开管理：

- 会话：对应一个消息来源（例如某个群/私聊），以 `unified_msg_origin (umo)` 作为标识
- 对话分支：同一会话下可创建多个分支，并支持切换/删除

这套机制直接影响：上下文历史、人格（persona）选择、以及 Agent 的工具循环输入。

## `ConversationManager` 常用操作

- `new_conversation(umo, content=None, title=None, persona_id=None) -> str`：新建对话分支，返回 conversation_id（UUID）
- `switch_conversation(umo, conversation_id)`：切换当前会话的活动分支
- `delete_conversation(umo, conversation_id=None)`：删除对话分支（不传 id 通常表示删除当前分支）
- `get_curr_conversation_id(umo) -> str | None`：获取当前活动分支 id
- `get_conversation(umo, conversation_id, create_if_not_exists=False)`：读取对话对象
- `get_conversations(umo=None, platform_id=None)`：列出对话
- `update_conversation(umo, conversation_id, history=None, title=None, persona_id=None)`：更新历史/标题/persona
- `get_human_readable_context(...)`：分页获取可读上下文

## 常见联动点

- 人格选择与禁用：`docs/agent/persona-resolution.md`
- 上下文压缩策略（截断/摘要）：`docs/agent/context-compression.md`

## 相关源码位置

- ConversationManager：`astrbotcore/astrbot/core/conversation_mgr.py`
- Session/Conversation 数据模型：`astrbotcore/astrbot/core/db/po.py`
