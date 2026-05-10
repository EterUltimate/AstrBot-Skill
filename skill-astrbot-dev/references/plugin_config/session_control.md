---
category: plugin_config
---

# 会话控制 (Session Control)

AstrBot 提供会话等待机制，允许插件暂停处理流程，等待同一会话的后续消息。

## session_waiter 装饰器

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("confirm")
async def confirm_action(self, event: AstrMessageEvent):
    yield event.plain_result("请输入 yes/no 确认操作：")
    
    @event.session_waiter(timeout=60, session_filter=None)
    async def wait_for_confirm(event2: AstrMessageEvent):
        answer = event2.message_str.strip().lower()
        if answer == "yes":
            yield event2.plain_result("操作已确认！")
        else:
            yield event2.plain_result("操作已取消。")
```

### 参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `timeout` | `int` | 超时秒数，默认 60 |
| `session_filter` | `SessionFilter \| None` | 会话过滤器，默认按 `unified_msg_origin` 匹配 |

## SessionController

`session_waiter` 内部创建的控制器对象，可通过闭包或装饰器机制访问：

```python
@filter.command("chat_loop")
async def chat_loop(self, event: AstrMessageEvent):
    yield event.plain_result("进入对话模式，输入 exit 退出。")
    
    @event.session_waiter(timeout=120)
    async def loop(event2: AstrMessageEvent, controller: SessionController):
        if event2.message_str.strip() == "exit":
            controller.stop()
            yield event2.plain_result("已退出对话模式。")
        else:
            # 处理消息
            yield event2.plain_result(f"收到：{event2.message_str}")
            controller.keep()  # 保持等待下一条消息
```

### SessionController 方法

| 方法 | 说明 |
| :--- | :--- |
| `keep()` | 继续等待下一条消息 |
| `stop()` | 停止等待，结束会话控制 |
| `get_history_chains() -> list[MessageChain]` | 获取本次会话等待期间收集的所有消息链 |

### get_history_chains 返回值

返回 `list[MessageChain]`，每个元素是一次用户输入的完整消息链。可用于：
- 会话结束后汇总处理
- 统计/审计用户输入
- 批量操作（如收集多张图片后统一处理）

```python
@event.session_waiter(timeout=30)
async def collect_images(event2: AstrMessageEvent, controller: SessionController):
    images = [c for c in event2.get_result().chain if isinstance(c, Image)]
    if len(images) >= 3:
        all_chains = controller.get_history_chains()
        # 处理所有收集到的消息
        controller.stop()
    else:
        controller.keep()
```

## SessionFilter

自定义会话匹配逻辑，控制哪些消息会进入 `session_waiter` 的回调：

```python
from astrbot.api.event import SessionFilter

# 默认：按 unified_msg_origin 匹配（同一会话）
# 自定义：按群 ID 匹配（同一群的任意用户消息都会触发）
class GroupSessionFilter(SessionFilter):
    def filter(self, event: AstrMessageEvent) -> str:
        # 返回会话标识字符串，相同标识的消息才会进入回调
        return event.get_group_id() or event.unified_msg_origin

@filter.command("group_poll")
async def group_poll(self, event: AstrMessageEvent):
    yield event.plain_result("群投票开始，请回复你的选择：")
    
    @event.session_waiter(timeout=60, session_filter=GroupSessionFilter())
    async def collect_votes(event2: AstrMessageEvent, controller: SessionController):
        # 同一群里任何人的回复都会进入这里
        controller.keep()
```

## 注意事项

- `session_waiter` 是协程级别的等待，不会阻塞事件循环。
- 超时后回调不会再被触发，需要做好超时后的清理逻辑。
- 同一会话同时只能有一个 `session_waiter` 活跃，新的会覆盖旧的。
