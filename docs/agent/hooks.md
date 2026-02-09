---
category: agent
---

# Hooks（事件钩子 vs Agent 运行钩子）

AstrBot 里经常被称为 “hook” 的东西至少有两套：

1) **事件钩子（Plugin Event Hooks）**：`@filter.on_*`  
   - 面向插件开发者，用于在核心流程节点介入（LLM 请求、工具调用、发消息前后等）
   - 文档：`docs/plugin_config/hooks.md`

2) **Agent 运行钩子（Agent Runner Hooks）**：`BaseAgentRunHooks`  
   - 面向更底层的 Agent 扩展/框架开发，用于在工具循环 runner 的关键时刻介入
   - 本文档重点讲这一层

## `BaseAgentRunHooks` 接口

核心接口定义在：

- `astrbotcore/astrbot/core/agent/hooks.py`

常用方法（以代码为准）：

- `on_agent_begin(run_context)`
- `on_tool_start(run_context, tool, tool_args)`
- `on_tool_end(run_context, tool, tool_args, tool_result)`
- `on_agent_done(run_context, llm_response)`

### 典型调用顺序（工具循环 runner）

以 `ToolLoopAgentRunner` 为例（源码：`astrbotcore/astrbot/core/agent/runners/tool_loop_agent_runner.py`），典型顺序是：

1. `on_agent_begin`
2. （循环）`on_tool_start` → 执行工具 → `on_tool_end`
3. `on_agent_done`

> 你应该把 run hook 当成“观测/装饰层”，不要在这里偷偷实现权限绕过或做不可控的副作用。

## 事件钩子与 Agent run hooks 的联动

主 Agent 默认会把部分 Agent 生命周期映射到事件钩子（用于给插件侧统一扩展点）：

- `astrbotcore/astrbot/core/astr_agent_hooks.py`
  - `on_tool_start` → 触发 `EventType.OnUsingLLMToolEvent`（对应 `@filter.on_using_llm_tool()`）
  - `on_tool_end` → 触发 `EventType.OnLLMToolRespondEvent`（对应 `@filter.on_llm_tool_respond()`）
  - `on_agent_done` → 触发 `EventType.OnLLMResponseEvent`（对应 `@filter.on_llm_response()`）

因此你在排查“某个 hook 没触发”时要先确认：

- 你用的是事件钩子还是 Agent run hook
- 当前执行路径是否走了工具循环 runner（以及是否配置了 hooks 对象）

## 相关源码位置（快速定位）

- Agent hooks 接口：`astrbotcore/astrbot/core/agent/hooks.py`
- 工具循环 runner：`astrbotcore/astrbot/core/agent/runners/tool_loop_agent_runner.py`
- 主 Agent hooks 映射：`astrbotcore/astrbot/core/astr_agent_hooks.py`
- 事件 hooks 注册与 EventType：`astrbotcore/astrbot/core/star/register/star_handler.py`、`astrbotcore/astrbot/core/star/star_handler.py`
