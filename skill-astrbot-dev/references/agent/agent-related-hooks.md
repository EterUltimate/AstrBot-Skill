---
category: agent
---

# Agent 相关钩子 (Agent-Related Hooks)

AstrBot 有两套钩子机制：
1. **插件事件钩子** — 装饰器注册，贯穿核心流程（LLM 请求前后、工具调用前后、消息发送前后）。详见 `plugin_config/hooks.md`。
2. **Agent 运行钩子** — 类继承注册，专用于 `tool_loop_agent` 执行周期的细粒度控制。

---

## 插件事件钩子（与 Agent 相关部分）

以下钩子在 `tool_loop_agent` 流程中的关键节点触发，通过 `@filter.*` 装饰器注册：

| 钩子 | 触发时机 | 签名 |
| :--- | :--- | :--- |
| `on_waiting_llm_request` | 确定调用 LLM，尚未获取会话锁 | `(self, event)` |
| `on_agent_begin` | Agent 工具循环开始前 (>=v4.23.1) | `(self, event)` |
| `on_using_llm_tool` | 函数工具调用前 | `(self, event, tool, tool_args)` |
| `on_llm_tool_respond` | 函数工具调用后 | `(self, event, tool, tool_args, tool_result)` |
| `on_agent_done` | Agent 工具循环完成后 (>=v4.23.1) | `(self, event)` |

```python
from astrbot.api.event import filter, AstrMessageEvent

class MyPlugin(Star):
    @filter.on_agent_begin()
    async def on_begin(self, event: AstrMessageEvent):
        logger.info("Agent 开始执行")

    @filter.on_using_llm_tool()
    async def on_tool_use(self, event, tool, tool_args):
        logger.info(f"调用工具: {tool.name}, 参数: {tool_args}")

    @filter.on_agent_done()
    async def on_done(self, event: AstrMessageEvent):
        logger.info("Agent 执行完成")
```

---

## Agent 运行钩子 (BaseAgentRunHooks)

通过类继承实现，用于 `tool_loop_agent` 的 `agent_hooks` 参数：

```python
from astrbot.core.agent.agent import BaseAgentRunHooks, AstrAgentContext

class MyAgentHooks(BaseAgentRunHooks):
    async def on_agent_begin(self, agent_context: AstrAgentContext):
        """Agent 循环开始前"""
        pass

    async def on_tool_start(self, agent_context: AstrAgentContext, tool_name: str, tool_args: dict):
        """工具调用前"""
        pass

    async def on_tool_end(self, agent_context: AstrAgentContext, tool_name: str, tool_args: dict, tool_result):
        """工具调用后"""
        pass

    async def on_agent_done(self, agent_context: AstrAgentContext):
        """Agent 循环结束后"""
        pass
```

### 使用方式

```python
hooks = MyAgentHooks()
result = await provider.tool_loop_agent(
    prompt="...",
    tools=[...],
    contexts=[],
    agent_hooks=hooks,       # 注入钩子
    agent_context=agent_ctx,  # 可选：注入上下文
)
```

### 默认映射

AstrBot 内部默认的 `BaseAgentRunHooks` 实现：
- `on_agent_begin` / `on_agent_done`：触发对应的插件事件钩子（`@filter.on_agent_begin()` / `@filter.on_agent_done()`）。
- `on_tool_start`：触发 `@filter.on_using_llm_tool()`。
- `on_tool_end`：触发 `@filter.on_llm_tool_respond()`。

> 自定义 `agent_hooks` 会替换默认实现。如果仍需默认行为，在自定义钩子中显式调用 `super()`。

---

## 两套钩子的选择

| 场景 | 推荐方式 |
| :--- | :--- |
| 插件级全局拦截/审计 | 插件事件钩子（`@filter.*`） |
| 特定 Agent 调用的细粒度控制 | Agent 运行钩子（`BaseAgentRunHooks`） |
| 需要访问 `AstrAgentContext` | Agent 运行钩子 |
| 简单日志/通知 | 插件事件钩子 |
