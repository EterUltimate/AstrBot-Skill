---
category: agent
---

# 注册工具 (Register Tools)

AstrBot 支持通过装饰器或数据类向 LLM 注册可调用工具（Function Calling / Tools Use）。

## FunctionTool 数据类

```python
from astrbot.api.provider import FunctionTool

@dataclass
class FunctionTool:
    name: str                       # 工具名（全局唯一）
    description: str                # 工具描述（LLM 可见）
    parameters: dict                # JSON Schema 格式参数定义
    func: Callable                  # 实际执行函数
    func_kwargs: dict | None        # 透传给 func 的额外参数
```

## ToolExecResult

工具执行返回值：

```python
from astrbot.api.provider import ToolExecResult

@dataclass
class ToolExecResult:
    result: str | None              # 工具执行结果文本
    is_error: bool = False          # 是否为错误结果
    image_url: str | None = None    # 可选：返回图片 URL
```

- `is_error=True` 时，LLM 会将结果视为工具调用失败，可能重试或告知用户。
- `image_url` 不为 None 时，图片会被注入到 LLM 上下文中（多模态模型可直接"看到"图片）。

## 方式 1：装饰器注册

最常用方式，AstrBot 自动从函数签名和 docstring 解析参数：

```python
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import ToolExecResult

@register("my_plugin", "Author", "示例插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("search")
    async def search(self, event: AstrMessageEvent, query: str, limit: int = 5):
        """搜索信息
        args:
            query: 搜索关键词
            limit: 返回数量上限
        """
        results = await do_search(query, limit)
        yield event.plain_result(str(results))
```

Docstring 中的 `args:` 部分会自动解析为 `FunctionTool.parameters`。

## 方式 2：ToolSet 批量注册

将多个工具打包为 ToolSet，一次性注册：

```python
from astrbot.api.provider import ToolSet

tools = ToolSet(
    name="web_tools",
    tools=[
        FunctionTool(name="search", description="搜索", parameters={...}, func=search_func),
        FunctionTool(name="browse", description="浏览网页", parameters={...}, func=browse_func),
    ]
)
```

## 方式 3：全局注册

不依赖 Star 类，直接注册到 Context：

```python
from astrbot.api.provider import FunctionTool

func_tool = FunctionTool(
    name="calculate",
    description="执行数学计算",
    parameters={
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "数学表达式"}
        },
        "required": ["expression"]
    },
    func=calculate,
)
self.context.register_tool(func_tool)
```

## 返回图片结果示例

```python
@filter.command("chart")
async def generate_chart(self, event: AstrMessageEvent, data: str):
    """生成图表
    args:
        data: 图表数据（JSON 格式）
    """
    image_path = await render_chart(data)
    return ToolExecResult(
        result="图表已生成",
        image_url=f"file://{image_path}",
    )
```

## 返回错误结果示例

```python
@filter.command("api_call")
async def call_api(self, event: AstrMessageEvent, endpoint: str):
    """调用 API
    args:
        endpoint: API 端点
    """
    try:
        result = await fetch_api(endpoint)
        yield event.plain_result(result)
    except Exception as e:
        yield ToolExecResult(result=f"API 调用失败: {e}", is_error=True)
```

## MUST

- 工具名全局唯一，重复注册会覆盖。
- `parameters` 必须符合 JSON Schema `object` 类型规范。
- 工具函数应为 `async`，签名中可包含 `event: AstrMessageEvent` 作为第一个参数。
- docstring `args:` 格式：`参数名: 描述`，每行一个。
