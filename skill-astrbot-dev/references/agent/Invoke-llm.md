---
category: agent
---

# 调用 LLM (Invoke LLM)

插件侧通过 `self.context` 访问 LLM Provider 和 Agent Runner。

## 1) 获取 Provider

```python
# 获取当前使用的 Chat Provider
provider = self.context.get_using_provider()

# 按 ID 获取
provider = self.context.get_provider_by_id("openai-gpt4")
```

## 2) llm_generate

```python
result = await provider.llm_generate(
    prompt="Hello",
    contexts=[],              # OpenAI 风格消息历史 list[dict]
    image_urls: list[str] = [],   # 图片 URL 列表（多模态模型）
    system_prompt: str | None = None,
    **kwargs
)
```

- `contexts`：可选。提供上下文消息历史，不传则只发单轮。
- `image_urls`：可选。向多模态模型注入图片（URL 格式，`https://` 或本地 `file://`）。
- 返回 `LLMResponse` 对象。

## 3) tool_loop_agent（推荐）

AstrBot v4.22.2+ 的 Agent 工具循环，支持多轮工具调用和完整 Agent 流程：

```python
result = await self.context.get_using_provider().tool_loop_agent(
    prompt="帮我查天气",
    tools=[],                     # FunctionTool 列表
    contexts=[],                  # 消息历史
    system_prompt=None,           # 系统提示词
    max_rounds=10,                # 最大工具调用轮数
    **kwargs,                     # v4.22.2+ 扩展参数
)
```

### v4.22.2+ **kwargs 扩展参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `stream` | `bool` | 是否流式输出 |
| `agent_hooks` | `BaseAgentRunHooks \| None` | Agent 运行钩子实例 |
| `agent_context` | `AstrAgentContext \| None` | Agent 上下文对象 |

```python
from astrbot.core.agent.agent import AstrAgentContext

agent_ctx = AstrAgentContext(
    event=event,
    provider=provider,
    conversation_id=cid,
)

result = await provider.tool_loop_agent(
    prompt="分析这段代码",
    tools=my_tools,
    contexts=history,
    system_prompt="你是一个代码审查专家",
    max_rounds=5,
    stream=True,
    agent_context=agent_ctx,
)
```

## 4) 传统 Provider 方法

```python
# 直接对话
resp = await provider.text_chat(prompt, contexts, system_prompt=system_prompt)

# 带图片的对话（多模态）
resp = await provider.text_chat_with_image(prompt, image_urls, contexts)
```

> 传统方法功能有限，建议优先使用 `tool_loop_agent` 或 `llm_generate`。

## 5) 多 Agent（Agent-as-Tool）

将一个 Agent 作为另一个 Agent 的工具使用：

```python
# 子 Agent 的工具集
sub_tools = [search_tool, browse_tool]

# 主 Agent 调用
result = await provider.tool_loop_agent(
    prompt="帮我调研一下...",
    tools=[...],  # 主 Agent 的工具（可包含子 Agent 包装的工具）
    contexts=[],
)
```

> 具体的 Agent-as-Tool 封装模式参见 `agent/subagents.md`。
