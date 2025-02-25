# 消息平台适配器

## aiocqhttp

```json{2,3,4}
{
    "id": "default",
    "type": "aiocqhttp",
    "enable": false,
    "ws_reverse_host": "",
    "ws_reverse_port": 6199
}
```

其中，高亮的配置项是所有的适配器配置都有的配置项，`id` 是适配器的唯一标识符，`type` 是适配器的类型，`enable` 是适配器是否启用的标志。

- `ws_reverse_host` 反向 WebSocket 的主机地址。
- `ws_reverse_port` 反向 WebSocket 的端口。

## qqofficial

```json
{
    "id": "default",
    "type": "qq_official",
    "enable": false,
    "appid": "",
    "secret": "",
    "enable_group_c2c": true,
    "enable_guild_direct_message": true
}
```

- `appid` QQ 官方机器人的 appid。
- `secret` QQ 官方机器人的 secret。
- `enable_group_c2c` 是否启用 QQ 私聊。
- `enable_guild_direct_message` 是否启用 QQ 群聊。

## vchat

```json
{
    "id": "default",
    "type": "vchat",
    "enable": false
}
```