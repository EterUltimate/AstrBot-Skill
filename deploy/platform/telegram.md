
# 接入 Telegram

## 1. 创建 Telegram Bot

首先，打开 Telegram，搜索 `BotFather`，点击 `Start`，然后发送 `/newbot`，按照提示输入你的机器人名字和用户名。

创建成功后，`BotFather` 会给你一个 `token`，请妥善保存。

## 2. 配置 AstrBot

打开 AstrBot 的管理面板，选择左边栏的 `消息平台适配器` 选项卡。点击 `+` 号，选择 `Telegram`，会出现 `Telegram` 的相关配置项，将 `token` 填入 `Bot Token` 中即可。

请确保你的网络环境可以访问 Telegram。你可能需要使用 `配置->其他配置->HTTP 代理` 来设置代理。