---
category: plugin_config
---

# 配置 Schema (`_conf_schema.json`)

AstrBot 通过 Schema 实现配置的自动解析与 WebUI 可视化渲染。

### 配置定义

在插件目录下添加 `_conf_schema.json` 文件，定义配置项的 Schema。

### 字段说明

| 字段名 | 说明 |
| :--- | :--- |
| `type` | **必填**。支持 `string`, `text`, `int`, `float`, `bool`, `object`, `list`, `dict`, `template_list`, `file` |
| `description` | 配置描述 |
| `hint` | 提示语，右侧问号图标悬浮显示 |
| `obvious_hint` | 是否醒目显示 |
| `default` | 默认值 |
| `options` | 下拉列表可选项 |
| `items` | `object` 类型的子 Schema |
| `editor_mode` | 启用代码编辑器 (Monaco Editor) |
| `editor_language` | 代码编辑器语言，默认 `json` |
| `editor_theme` | 代码编辑器主题，`vs-light` 或 `vs-dark` |
| `_special` | 调用内置数据：`select_provider`, `select_provider_tts`, `select_provider_stt`, `select_persona`, `select_knowledgebase` |
| `invisible` | 是否隐藏，默认 `false` |

### 高级类型

- **`text`**: 多行文本输入
- **`dict`**: 键值对配置，支持 `template_schema` 定义子项
- **`template_list`**: 多组重复配置（v4.10.4+）
- **`file`**: 文件上传配置（v4.13.0+）

### `dict` 类型

使用 `template_schema` 定义 dict 内部子项的结构：

```json
{
  "api_config": {
    "type": "dict",
    "description": "API 配置",
    "template_schema": {
      "endpoint": {"description": "API 地址", "type": "string", "default": "https://api.example.com"},
      "timeout": {"description": "超时时间(秒)", "type": "int", "default": 30}
    }
  }
}
```

支持 `slider` 子字段用于数值滑块：

```json
{
  "temperature": {
    "type": "float",
    "description": "温度参数",
    "default": 0.7,
    "slider": {
      "min": 0,
      "max": 2,
      "step": 0.1
    }
  }
}
```

### `template_list` 类型

用于保存多组重复配置，如多个 API 供应商或多套人设。

```json
{
  "providers": {
    "type": "template_list",
    "description": "API 供应商列表",
    "templates": {
      "openai": {
        "name": "OpenAI",
        "items": {
          "api_key": {"description": "API Key", "type": "string", "default": "sk-xxxx"},
          "model": {"description": "模型名称", "type": "string", "default": "gpt-3.5-turbo"}
        }
      }
    }
  }
}
```

存储格式（包含 `__template_key` 字段）：

```json
{
  "providers": [
    {"__template_key": "openai", "api_key": "sk-xxxx", "model": "gpt-3.5-turbo"}
  ]
}
```

### `file` 类型（>= v4.13.0）

用于文件上传，支持类型白名单过滤：

```json
{
  "model_file": {
    "type": "file",
    "description": "模型权重文件",
    "file_types": [".onnx", ".pt", ".bin"]
  }
}
```

- 上传文件统一存储在 `data/plugins/<plugin_name>/files/<config_key_path>/`
- 文件名经过 `sanitize_filename` 清洗，防止路径穿越
- 配置中保存的值为相对路径（`files/...` 开头）
- 系统级限制上传文件大小，默认 500MB
- 详见 `plugin_config/file_config.md`

### `_special` 内置数据选择器

| `_special` 值 | 说明 |
| :--- | :--- |
| `select_provider` | 下拉选择 Chat Provider |
| `select_provider_tts` | 下拉选择 TTS Provider |
| `select_provider_stt` | 下拉选择 STT Provider |
| `select_persona` | 下拉选择人设 |
| `select_knowledgebase` | 下拉选择知识库 |

### i18n 支持

Schema 中的 `description`、`hint`、`options` 的 label 字段支持 i18n 键（以 `i18n:` 前缀开头），配合 `.astrbot-plugin/i18n/*.json` 实现多语言：

```json
{
  "api_key": {
    "description": "i18n:config.api_key.desc",
    "type": "string"
  }
}
```

### 在插件中使用

```python
from astrbot.api import AstrBotConfig

@register("config", "Soulter", "一个配置示例", "1.0.0")
class ConfigPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        # self.config.save_config()  # 保存配置
```

配置更新时，AstrBot 会自动添加缺失的默认值、移除不存在的配置项。
