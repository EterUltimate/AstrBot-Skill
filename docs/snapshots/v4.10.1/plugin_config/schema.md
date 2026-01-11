---
category: plugin_config
---

# 配置 Schema (`_conf_schema.json`)

AstrBot 通过 Schema 实现配置的自动解析与 WebUI 可视化渲染。

### 核心字段与 UI 对应关系

| 字段名 | 类型 | 说明 | UI 表现 |
| :--- | :--- | :--- | :--- |
| `type` | `string` | **必填**。支持 `string`, `text`, `int`, `float`, `bool`, `object`, `list`, `dict`, `template_list` | 基础输入框、开关或嵌套面板 |
| `description` | `string` | 配置描述 | 配置项下方的文字说明 |
| `hint` | `string` | 提示语 | 右侧问号图标，悬浮显示 |
| `obvious_hint` | `bool` | 是否醒目显示 | 醒目的提示框 |
| `default` | `any` | 默认值 | 初始填充值 |
| `options` | `list` | 可选项 | 下拉选择框 (Select) |
| `items` | `object` | 类型为 `object` 时的子 Schema | 嵌套折叠面板 |
| `editor_mode` | `bool` | 是否启用代码编辑器 | 切换为 Monaco Editor |
| `_special` | `string` | 调用内置数据 | 下拉选择 `select_provider`, `select_persona` 等 |

### 高级类型说明

- **`text`**: 渲染为多行 `textarea`。
- **`dict`**: 允许用户以键值对形式添加配置。支持 `template_schema` 定义子项。
- **`template_list`**: 允许用户根据多个预设模板（`templates`）添加列表项。
- **`template_schema`**: 提供可选的模板字段及其滑块 (`slider`) 控制。
