---
category: plugin_config
---

# 最小插件示例 (Simple Plugin)

一个 AstrBot 插件的最小实现，包含核心概念。

## 最小示例

```python
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent

@register("hello_world", "Author", "Hello World 插件", "1.0.0")
class HelloWorldPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("hello")
    async def hello(self, event: AstrMessageEvent):
        yield event.plain_result("Hello, World!")

    async def terminate(self):
        """插件卸载时的清理逻辑（可选）"""
        pass
```

## 核心概念

### Star 类

所有插件必须继承 `Star` 基类：

```python
from astrbot.api.star import Star

class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
```

### Context

`Context` 是插件与 AstrBot 核心交互的主要接口：

```python
# 访问 Context
ctx = self.context

# 常用方法
ctx.get_using_provider()          # 获取当前 LLM Provider
ctx.get_using_provider().tool_loop_agent(...)  # Agent 调用
ctx.conversation_manager          # 会话管理
ctx.persona_manager               # 人设管理
ctx.register_tool(func_tool)      # 注册工具
```

### AstrMessageEvent

事件对象，包含用户消息和会话信息：

```python
@filter.command("echo")
async def echo(self, event: AstrMessageEvent):
    # 获取消息文本
    text = event.message_str

    # 获取发送者 ID
    sender = event.get_sender_id()

    # 获取会话标识
    umo = event.unified_msg_origin

    # 发送结果
    yield event.plain_result(f"你说: {text}")

    # 或使用链式结果
    yield event.chain_result([Comp.Plain("复杂消息")])
```

### @register 装饰器

```python
@register(
    "plugin_name",       # 唯一标识（小写+下划线）
    "Author Name",       # 作者
    "插件描述",          # 简短描述
    "1.0.0",            # 版本号
)
```

### @filter 装饰器

注册消息处理器：

```python
# 命令触发
@filter.command("hello")
async def hello(self, event: AstrMessageEvent):
    ...

# 正则匹配
@filter.regex(r"^\d+$")
async def on_number(self, event: AstrMessageEvent):
    ...

# 所有消息
@filter.message_event()
async def on_message(self, event: AstrMessageEvent):
    ...
```

### terminate 方法

插件卸载时调用，用于清理资源：

```python
async def terminate(self):
    # 关闭连接、取消定时任务等
    await self.db.close()
```

## 结果返回方式

```python
# 纯文本
yield event.plain_result("文本内容")

# 消息链
import astrbot.api.message_components as Comp
yield event.chain_result([
    Comp.At(user_id=event.get_sender_id()),
    Comp.Plain(" 消息内容"),
])

# 主动发送（不在 yield 流程中）
await event.send(Comp.Plain("通知消息"))
```
