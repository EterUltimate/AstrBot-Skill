---
category: agent
---

# Cron（定时任务 / 主动能力）

AstrBot 支持通过定时任务唤醒 Agent 执行任务（proactive agent）。典型场景：每日推送、定时巡检、订阅信息汇总等。

## 两个层面

1) **CronJobManager（调度层）**：负责解析 cron 表达式、调度执行、持久化任务定义  
2) **Agent 工具层（运维层）**：主 Agent 可注入“创建/删除/列出 cron job”的工具，便于在对话中自助管理

## 关键实现入口

- CronJobManager：`astrbotcore/astrbot/core/cron/manager.py`
- Cron 事件：`astrbotcore/astrbot/core/cron/events.py`（`CronMessageEvent`）
- Cron 工具：`astrbotcore/astrbot/core/tools/cron_tools.py`
- 主 Agent 注入 cron tools：`astrbotcore/astrbot/core/astr_main_agent.py`（`add_cron_tools`）

## 常见配置键（名称对齐）

- `provider_settings.proactive_capability.add_cron_tools`: 是否向主 Agent 注入 cron 管理工具

默认配置入口：

- `astrbotcore/astrbot/core/config/default.py`

## 典型注意事项

- cron 唤醒不是用户消息：system prompt 通常需要明确“为什么被唤醒、应该做什么、是否需要联系用户”
- 定时任务要可重试/可幂等：避免重复推送、重复执行副作用
- 如果任务需要外部访问或执行代码，优先配合 sandbox runtime（见 `docs/agent/sandbox.md`）
