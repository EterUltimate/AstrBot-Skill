---
outline: deep
---


# AstrBot 配置文件

AstrBot 的配置文件是一个 `Json` 格式的文件。AstrBot 会在启动时读取这个文件，并根据文件中的配置来初始化 AstrBot。

它位于 `data/cmd_config.json` 下。接下来，我们将详细介绍 AstrBot 的配置文件。


AstrBot 默认配置如下：

```json
{
    "config_version": 2,
    "platform_settings": {
        "unique_session": false,
        "rate_limit": {
            "time": 60,
            "count": 30,
            "strategy": "stall",
        },
        "reply_prefix": "",
        "forward_threshold": 200,
        "id_whitelist": [],
        "wl_ignore_admin_on_group": true,
        "wl_ignore_admin_on_friend": true
    },
    "provider": [],
    "provider_settings": {
        "enable": true,
        "wake_prefix": "",
        "web_search": false,
        "identifier": false,
        "datetime_system_prompt": true,
        "default_personality": "如果用户寻求帮助或者打招呼，请告诉他可以用 /help 查看 AstrBot 帮助。",
        "prompt_prefix": ""
    },
    "content_safety": {
        "internal_keywords": {"enable": true, "extra_keywords": []},
        "baidu_aip": {"enable": false, "app_id": "", "api_key": "", "secret_key": ""}
    },
    "admins_id": [],
    "t2i": false,
    "http_proxy": "",
    "dashboard": {
        "enable": true,
        "username": "astrbot",
        "password": "77b90590a8945a7d36c963981a307dc9"
    },
    "platform": [],
    "wake_prefix": ["/"],
    "log_level": "INFO",
    "t2i_endpoint": "",
    "pip_install_arg": "",
    "plugin_repo_mirror": ""
}
```

## 字段

### `config_version`

配置文件版本。请勿修改。

### `platform`

一个列表，存储了 AstrBot 的消息平台适配器配置。当前，AstrBot 默认支持的消息平台适配器有 `aiocqhttp`、`qqofficial`、`vchat`。如果你想通过修改配置文件的方式新增消息平台适配器，可以根据需要复制下面的配置并添加到这个列表中。

由于配置较多，具体配置请参考 [消息平台适配器](/config/platform)。

> [!TIP]
> 如果你不会 Json 语法，可以使用在线的 [Json 编辑器](https://jsoneditoronline.org/) 来编辑配置文件。当有语法错误，会有提示。



### `platform_settings`

消息平台适配器的通用设置。

- `unique_session`: 是否启用唯一会话。默认为 `false`。启用后，在群组或者频道中，每个人的消息上下文都是独立的。

- `rate_limit`: 当消息速率超过限制时的处理策略。`time` 为时间窗口，`count` 为消息数量，`strategy` 为限制策略。`stall` 为等待，`discard` 为丢弃。 

- `reply_prefix`: 回复消息时的固定前缀字符串。默认为空。

- `forward_threshold`: 消息转发阈值。当回复内容超过一定字数后，机器人会将消息折叠成 QQ 群聊的 “转发消息”，以防止刷屏。目前仅 QQ 平台适配器适用。

- `id_whitelist`: ID 白名单。填写后，将只处理所填写的 ID 发来的消息事件。为空时表示不启用白名单过滤。可以使用 /myid 指令获取在某个平台上的会话 ID。也可在 AstrBot 日志内获取会话 ID，当一条消息没通过白名单时，会输出 INFO 级别的日志。会话 ID 类似 aiocqhttp:GroupMessage:547540978

- `wl_ignore_admin_on_group`: 是否管理员发送的群组消息无视 ID 白名单。默认为 `true`。

- `wl_ignore_admin_on_friend`: 是否管理员发送的私聊消息无视 ID 白名单。默认为 `true`。

### `provider`

和 `platform` 一样也是一个列表，存储了大语言模型提供商的配置。

由于配置较多，具体配置请参考 [大语言模型提供商](/config/provider)。

> [!TIP]
> 使用 `/provider` 指令可以查看、切换大语言模型提供商。
> 
> 使用 `/model` 指令可以查看、切换提供商支持的模型。（需要提供商适配）


### `provider_settings`

大语言模型提供商的通用设置。

- `enable`: 是否启用大语言模型聊天。默认为 `true`。
- `wake_prefix`: 使用 LLM 聊天额外的触发条件。如填写 `chat`，则需要发送消息时要以 `/chat` 才能触发 LLM 聊天。其中 `/` 是机器人的唤醒前缀。是一个防止滥用的手段。
- `web_search`: 是否启用 Web 搜索。默认为 `false`。启用后，LLM 可能会自动搜索网页并根据内容回答。能访问 Google 时效果最佳。如果 Google 访问失败，程序会依次访问 Bing, Sogo 搜索引擎。
- `identifier`: 在 Prompt 前加上群成员的名字以让模型更好地了解群聊状态。启用将略微增加 token 开销。
- `datetime_system_prompt`: 启用后，会在系统提示词中加上当前机器的日期时间。
- `default_personality`: 默认人格（情境设置/System Prompt）文本。也可以使用 `/persona` 指令来切换人格。
- `prompt_prefix`: 添加之后，会在每次对话的 Prompt 前加上此文本。默认为空。

### `content_safety`

内容安全设置。

- `internal_keywords`: 内部关键词检测。`enable` 是否启用内部关键词检测。`extra_keywords` 额外的关键词列表。**支持正则表达式。**
- `baidu_aip`: 百度 AI 内容审核。`enable` 是否启用百度 AI 内容审核。`app_id`, `api_key`, `secret_key` 为百度 AI 内容审核的配置。

> [!TIP]
> 如果要启用百度 AI 内容审核，请先 `pip install baidu-aip`。

### `admins_id`

管理员 ID 列表。此外，还可以使用 `/op`, `/deop` 指令来添加或删除管理员。

> [!TIP]
> aiocqhttp 的管理员 ID 是 QQ 号。

### `t2i`

启用后，超出一定长度的文本将会通过 AstrBot API 渲染成 Markdown 图片发送。可以缓解审核和消息过长刷屏的问题，并提高 Markdown 文本的可读性。

### `http_proxy`

HTTP 代理。如 `http://localhost:7890`。

### `dashboard`

请不要随意修改 `password` 的值。它是一个经过 `md5` 加密的密码。请在控制面板修改密码。

### `wake_prefix`

唤醒前缀。默认为 `/`。当消息以 `/` 开头时，AstrBot 会被唤醒。

> [!TIP]
> 还需要在白名单中。

### `log_level`

日志级别。默认为 `INFO`。可以设置为 `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`。

### `t2i_endpoint`

AstrBot API 的地址。用于渲染 Markdown 图片。

### `pip_install_arg`

`pip install` 的参数。如 `-i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`。

### `plugin_repo_mirror`

GitHub 仓库镜像。用于加速安装插件、AstrBot 更新。在控制面板中提供了可选项。
