---
category: plugin_config
---

# 开发环境 (Development Environment)

## 快速开始

### 1) 使用模板创建插件

推荐使用 helloworld 模板仓库：

```bash
# 克隆模板
git clone https://github.com/Soulter/helloworld.git my_plugin
cd my_plugin
```

### 2) 安装到 AstrBot

将插件目录放入 AstrBot 的插件目录：

```bash
# 方式 1：直接放入
cp -r my_plugin /path/to/AstrBot/data/plugins/

# 方式 2：符号链接（开发推荐）
ln -s /path/to/my_plugin /path/to/AstrBot/data/plugins/my_plugin
```

### 3) 热重载

AstrBot 支持插件热重载，修改代码后无需重启：

1. 打开 AstrBot 管理面板（WebUI）
2. 进入插件管理页面
3. 点击对应插件的"重载"按钮

> 热重载会重新执行 `__init__`，但不会重新加载 Python 模块。如修改了导入或新增了文件，建议完全重启 AstrBot。

## 依赖管理

### requirements.txt

在插件根目录放置 `requirements.txt`，AstrBot 会在安装/更新插件时自动安装依赖：

```
requests>=2.28.0
pillow>=9.0.0
beautifulsoup4
```

### 注意事项

- 依赖安装在 AstrBot 的 Python 环境中。
- 版本约束建议宽松（`>=` 而非 `==`），避免与其他插件冲突。
- 不建议安装大型 ML 库（如 `torch`），AstrBot 插件体积限制 32MB。
- 如需使用系统级依赖，在 `metadata.yaml` 中声明（实验性功能）。

## 插件目录规范

```
my_plugin/
├── main.py                  # 入口文件（必须）
├── _conf_schema.json        # 配置 Schema（可选）
├── requirements.txt         # Python 依赖（可选）
├── metadata.yaml            # 元数据（可选，AstrBot 会自动生成）
├── logo.png                 # 插件图标（可选，建议 256x256）
├── .astrbot-plugin/         # AstrBot 插件资源目录
│   ├── i18n/               # 国际化文件
│   │   ├── zh-CN.json
│   │   └── en-US.json
│   └── pages/              # Dashboard 页面
│       └── dashboard.html
├── skills/                  # 技能定义（可选）
│   └── my_skill/
│       └── SKILL.md
└── README.md               # 说明文档
```

### 关键文件说明

| 文件 | 必须 | 说明 |
| :--- | :--- | :--- |
| `main.py` | ✅ | 插件入口，包含 `@register` 装饰器和 Star 类 |
| `_conf_schema.json` | ❌ | 配置 Schema 定义 |
| `requirements.txt` | ❌ | Python 依赖声明 |
| `logo.png` | ❌ | 插件图标，显示在插件市场和管理面板 |
| `.astrbot-plugin/` | ❌ | i18n 和页面资源目录 |

## 入口文件 main.py

```python
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent

@register("my_plugin", "Author", "我的插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("hello")
    async def hello(self, event: AstrMessageEvent):
        yield event.plain_result("Hello, World!")
```

### @register 参数

| 参数 | 说明 |
| :--- | :--- |
| `name` | 插件唯一标识（英文，小写下划线） |
| `author` | 作者名 |
| `description` | 简短描述 |
| `version` | 版本号（语义化版本） |

## 开发原则

1. **入口文件必须命名为 `main.py`**：AstrBot 通过此文件发现和加载插件。
2. **最小依赖**：只引入必要的包，避免与其他插件冲突。
3. **异步优先**：所有 I/O 操作使用 `async/await`。
4. **错误隔离**：插件异常不应影响 AstrBot 核心和其他插件。
5. **配置驱动**：可变参数使用 `_conf_schema.json` 管理，不要硬编码。
