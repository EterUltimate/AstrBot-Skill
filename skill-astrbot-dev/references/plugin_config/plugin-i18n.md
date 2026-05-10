---
category: plugin_config
---

# 国际化 (i18n)

AstrBot 提供完整的插件国际化支持，通过 `.astrbot-plugin/i18n/` 目录下的 JSON 文件管理多语言翻译。

## 目录结构

```
your_plugin/
├── .astrbot-plugin/
│   └── i18n/
│       ├── zh-CN.json    # 简体中文
│       ├── en-US.json    # 英语（美国）
│       └── ja-JP.json    # 日语
├── main.py
└── _conf_schema.json
```

## i18n JSON 格式

```json
{
    "metadata": {
        "display_name": "我的插件",
        "short_desc": "一个示例插件",
        "desc": "这是一个更详细的描述"
    },
    "config": {
        "api_key": {
            "description": "API 密钥",
            "hint": "在官网获取"
        },
        "model": {
            "description": "模型名称",
            "options": {
                "gpt4": "GPT-4",
                "claude": "Claude"
            }
        }
    },
    "pages": {
        "dashboard": {
            "title": "仪表盘",
            "welcome": "欢迎使用"
        }
    },
    "commands": {
        "search": {
            "description": "搜索信息",
            "no_results": "没有找到结果"
        }
    }
}
```

## 元数据翻译 (metadata)

`metadata` 字段用于翻译插件的基本信息：

| 字段 | 说明 |
| :--- | :--- |
| `display_name` | 插件显示名称 |
| `short_desc` | 简短描述 |
| `desc` | 详细描述 |

这些翻译会覆盖 `@register()` 装饰器中的对应字段。

## 配置翻译 (config)

`config` 字段用于翻译 `_conf_schema.json` 中的配置项：

- `description`：配置项描述
- `hint`：提示文本
- `options.<key>.label`：下拉选项的显示文本

### Schema 中的 i18n 引用

在 `_conf_schema.json` 中使用 `i18n:` 前缀引用 i18n 键：

```json
{
    "api_key": {
        "description": "i18n:config.api_key.description",
        "hint": "i18n:config.api_key.hint",
        "type": "string"
    }
}
```

### template_list 的 i18n

```json
{
    "config": {
        "providers": {
            "openai": {
                "name": "OpenAI 供应商",
                "items": {
                    "api_key": {
                        "description": "API 密钥"
                    }
                }
            }
        }
    }
}
```

## 页面翻译 (pages)

Dashboard 页面的翻译通过 Bridge SDK 访问：

```javascript
// 在 Dashboard 页面中
const i18n = bridge.getI18n();
const t = bridge.t;

// 获取翻译文本
const title = t('pages.dashboard.title');

// 监听语言变化
bridge.onContext((ctx) => {
    const locale = ctx.locale;
    document.documentElement.lang = locale;
});
```

## 命令翻译 (commands)

命令的描述和响应文本翻译：

```python
# 在 Python 代码中，命令描述会自动从 i18n 加载
# 响应文本需要手动处理
from astrbot.api.star import Context

class MyPlugin(Star):
    async def get_localized_text(self, key: str) -> str:
        # 通过 context 获取当前语言环境
        locale = self.context.get_locale()
        return self.context.i18n_get(key, locale)
```

## Bridge SDK i18n 方法

Dashboard 页面（iframe）中通过 Bridge SDK 访问 i18n：

| 方法 | 说明 |
| :--- | :--- |
| `bridge.getI18n()` | 获取完整 i18n 对象 |
| `bridge.getLocale()` | 获取当前语言代码（如 `zh-CN`） |
| `bridge.t(key)` | 获取翻译文本 |
| `bridge.onContext(callback)` | 监听上下文变化（含语言切换） |

## 注意事项

- i18n JSON 文件必须以语言代码命名（如 `zh-CN.json`、`en-US.json`）。
- 缺少某个语言的翻译时，会回退到 `zh-CN`，再回退到键名本身。
- 修改 i18n 文件后需重新加载插件才能生效。
