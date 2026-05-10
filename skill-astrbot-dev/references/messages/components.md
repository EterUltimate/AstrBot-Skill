---
category: messages
---

# 消息链组件 (Message Components)

AstrBot 使用消息链（MessageChain）来描述消息结构，它是一个由多个消息段（MessagePart/Component）组成的有序列表。

### 核心组件及其兼容性

| 组件类型 | 描述 | 参数示例 | 平台兼容性建议 |
| :--- | :--- | :--- | :--- |
| `Plain` | 纯文本 | `text="Hello"` | 所有平台支持。 |
| `At` | 提及/艾特 | `user_id="xxx"` | 大多数平台支持。 |
| `Image` | 图片 | `fromFileSystem(path)`, `fromURL(url)` | 所有平台支持。URL 必须以 `http` 或 `https` 开头。 |
| `Record` | 语音 | `file="path/to/wav"` | 广泛支持。目前主要支持 `wav` 格式。 |
| `Video` | 视频 | `fromFileSystem(path)`, `fromURL(url)` | 广泛支持。常用格式为 `mp4` |
| `File` | 文件 | `file="path"`, `name="a.txt"` | 部分平台不支持。 |
| `Face` | 表情 | `id="123"` | 主要在 OneBot v11 (QQ) 平台支持。 |
| `Node/Nodes` | 合并转发节点 | `uin`, `name`, `content` | 仅 OneBot v11 支持。 |
| `Poke` | 戳一戳 | - | 主要在 OneBot v11 支持。 |
| `Reply` | 回复特定消息 | `message_id="xxx"` | 广泛支持。 |

### Video 组件

```python
from astrbot.api.message_components import Video

# 从本地文件
video = Video.fromFileSystem("/path/to/video.mp4")

# 从 URL
video = Video.fromURL("https://example.com/video.mp4")

# 方法
video.convert_to_file_path()  # -> str: 转换为本地路径
video.register_to_file_service()  # -> str: 注册到文件服务
```

### Node / Nodes 组件（合并转发消息）

用于 QQ 等平台的合并转发（长消息）功能：

```python
from astrbot.api.message_components import Node, Nodes, Plain

# 单条转发节点
node = Node(uin="123456", name="昵称", content=[Plain(text="转发的内容")])

# 多条转发节点
nodes = Nodes(nodes=[
    Node(uin="123456", name="用户A", content=[Plain(text="消息1")]),
    Node(uin="789012", name="用户B", content=[Plain(text="消息2")]),
])
```

### 消息构建示例

```python
import astrbot.api.message_components as Comp

# 方式 1：手动构建列表
chain = [
    Comp.At(user_id=event.get_sender_id()),
    Comp.Plain(" 来看这张图："),
    Comp.Image.fromURL("https://example.com/image.jpg")
]
yield event.chain_result(chain)

# 方式 2：使用 MessageChain 流式构建
from astrbot.api.event import MessageChain
message_chain = MessageChain().message("Hello!").file_image("path/to/image.jpg")
await self.context.send_message(event.unified_msg_origin, message_chain)
```

### MessageChain 构建器模式

`MessageChain` 支持链式调用构建复杂消息：

```python
from astrbot.api.event import MessageChain

chain = (MessageChain()
    .message("这是文本消息")
    .at(name="用户", qq="123456")
    .url_image("https://example.com/img.jpg")
    .file_image("/path/to/local/img.png")
    .base64_image("iVBORw0KGgo...")
    .use_t2i(True))  # 启用文本转图片
```

可用方法：

| 方法 | 说明 |
| :--- | :--- |
| `.message(text)` | 添加纯文本 |
| `.at(name, qq)` | 添加 At |
| `.at_all()` | 添加 AtAll |
| `.url_image(url)` | 添加网络图片 |
| `.file_image(path)` | 添加本地图片 |
| `.base64_image(b64)` | 添加 base64 图片 |
| `.use_t2i(bool)` | 设置是否使用文本转图片 |

工具方法：

- `get_plain_text(with_other_comps_mark: bool) -> str`: 获取纯文本
- `squash_plain()`: 合并所有 Plain 消息段
