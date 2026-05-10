---
category: plugin_config
---

# Dashboard 页面 (Plugin Pages)

AstrBot 支持插件注册自定义 Dashboard 页面，在管理面板中展示交互式 UI。

## 目录结构

```
your_plugin/
├── .astrbot-plugin/
│   ├── pages/
│   │   └── dashboard.html    # Dashboard 页面
│   └── i18n/
│       └── zh-CN.json
├── main.py
└── _conf_schema.json
```

## 注册页面

在 `main.py` 中通过装饰器注册：

```python
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter

@register("my_plugin", "Author", "示例插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
```

页面文件放在 `.astrbot-plugin/pages/` 目录下，AstrBot 会自动发现并注册。

## 页面开发

Dashboard 页面是标准 HTML 页面，运行在 iframe 中，通过 Bridge SDK 与 AstrBot 通信。

### 基本模板

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>My Dashboard</title>
    <script src="/__bridge__.js"></script>
</head>
<body>
    <div id="app">
        <h1 id="title">Loading...</h1>
    </div>
    <script>
        bridge.ready(async () => {
            const ctx = bridge.getContext();
            document.getElementById('title').textContent = bridge.t('pages.dashboard.title');
        });
    </script>
</body>
</html>
```

## Bridge SDK

页面通过 `<script src="/__bridge__.js"></script>` 加载 Bridge SDK。

### 核心方法

| 方法 | 返回值 | 说明 |
| :--- | :--- | :--- |
| `bridge.ready(callback)` | - | 页面就绪后执行回调 |
| `bridge.getContext()` | `object` | 获取当前上下文（locale, theme 等） |
| `bridge.getLocale()` | `string` | 获取当前语言代码 |
| `bridge.getI18n()` | `object` | 获取完整 i18n 翻译对象 |
| `bridge.t(key)` | `string` | 获取翻译文本 |
| `bridge.onContext(callback)` | - | 监听上下文变化（语言/主题切换） |

### API 请求方法

| 方法 | 参数 | 说明 |
| :--- | :--- | :--- |
| `bridge.apiGet(path, params?)` | `path: string, params?: object` | GET 请求 |
| `bridge.apiPost(path, body?)` | `path: string, body?: object` | POST 请求 |

### 文件操作方法

| 方法 | 参数 | 说明 |
| :--- | :--- | :--- |
| `bridge.upload(file, path?)` | `file: File, path?: string` | 上传文件 |
| `bridge.download(path)` | `path: string` | 下载文件 |

### SSE 订阅

| 方法 | 参数 | 说明 |
| :--- | :--- | :--- |
| `bridge.subscribeSSE(path, callback)` | `path: string, callback: Function` | 订阅 SSE 事件流 |
| `bridge.unsubscribeSSE(path)` | `path: string` | 取消 SSE 订阅 |

## 安全约束

Dashboard 页面运行在沙箱 iframe 中：

- 页面只能通过 Bridge SDK 与 AstrBot 通信，不能直接访问父页面。
- `apiGet`/`apiPost` 的路径受白名单限制，只能访问插件注册的 API 端点。
- 静态资源路径会被自动重写，确保资源从正确的插件目录加载。

## 静态资源

页面引用的静态资源（CSS、JS、图片）放在 `.astrbot-plugin/pages/` 下的任意子目录中：

```
.astrbot-plugin/pages/
├── dashboard.html
├── css/
│   └── style.css
├── js/
│   └── app.js
└── assets/
    └── logo.png
```

HTML 中的相对路径会被自动重写为正确的插件资源路径。

## SSE 实时更新示例

```html
<script>
bridge.ready(async () => {
    // 订阅实时状态
    bridge.subscribeSSE('/api/my_plugin/status', (event) => {
        const data = JSON.parse(event.data);
        document.getElementById('status').textContent = data.status;
    });
});

// 页面卸载时取消订阅
window.addEventListener('unload', () => {
    bridge.unsubscribeSSE('/api/my_plugin/status');
});
</script>
```

## 注意事项

- 页面必须在 iframe 中运行，不能独立打开。
- Bridge SDK 通过 `/__bridge__.js` 加载，路径固定。
- i18n 配合 `.astrbot-plugin/i18n/` 使用，详见 `plugin_config/plugin-i18n.md`。
