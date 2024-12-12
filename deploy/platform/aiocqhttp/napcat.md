# 通过 NapCatQQ 协议实现端接入 QQ

NapCatQQ 是基于无头 QQNT 的 OneBot 协议实现端。它本质上运行了一个 QQNT 实例。

NapCatQQ 的 GitHub 仓库：[NapCatQQ](https://github.com/NapNeko/NapCatQQ)
NapCatQQ 的文档：[NapCatQQ 文档](https://napcat.napneko.icu/)

> [!WARNING]
> 为了成功部署，你需要：
> - 一个 QQ 号（最好不是新创建的 QQ 号）。
> - 一台具有摄像功能的手机以扫码登录 QQ。

NapCat 提供了大量的部署方式，包括 Docker、Windows 一键安装包等等。在本篇文章里将以 Docker 部署为例。

## 通过 Docker 部署

默认您安装了 Docker。

在终端执行以下命令即可一键部署。

```bash
docker run -d \
-e NAPCAT_GID=$(id -g) \
-e NAPCAT_UID=$(id -u) \
-p 3000:3000 \
-p 3001:3001 \
-p 6099:6099 \
--name napcat \
--restart=always \
mlikiowa/napcat-docker:latest
```

执行成功后，需要查看日志以得到登录二维码和管理面板的 URL。

```bash
docker logs napcat
```

请复制管理面板的 URL，然后在浏览器中打开备用。

然后使用你要登录的 QQ 扫描出现的二维码，即可登录。

如果登录阶段没有出现问题，即成功部署。

## 连接到 AstrBot

### 配置 aiocqhttp

在 AstrBot 的管理面板中，选择左边栏的 `配置`，然后在右边的界面中，点击 `消息平台` 选项卡。点击 `+` 号，选择 `aiocqhttp`，会出现 `aiocqhttp` 的相关配置项，如下图所示：

![](../../../source/images/napcat/image.png)

配置项填写：

- ID(id)：随意填写，用于区分不同的消息平台实例。系统会自动填充。
- 启用(enable): 勾选。
- 反向 WebSocket 主机地址：请填写你的机器的 IP 地址。如 `0.0.0.0`
- 反向 WebSocket 端口：填写一个端口，例如 `6199`。

### 配置管理员

填写完毕后，点击 `其他配置` 选项卡，找到 `管理员 ID`，填写你的 QQ 号（不是机器人的 QQ 号）。

### 保存配置

切记点击右下角 `保存`，AstrBot 重启并会应用配置。

### 在 NapCatQQ 中添加 WebSocket 客户端

切换回 NapCatQQ 的管理面板，点击 `网络配置->添加网络配置`，在弹出的窗口中，名称随意填写，类型选择 `WebSocket 客户端`。点击确认。

![](../../../source/images/napcat/image-1.png)

在新弹出的窗口中：

- 勾选 `启用`。
- `URL` 填写 `ws://<宿主机IP>:<在 AstrBot中填写的端口>`。如 `ws://1.2.3.4:6199`。
- 消息格式：`Array`

点击 `保存`。

## 🎉 大功告成！

此时，你的 AstrBot 和 NapCatQQ 应该已经连接成功。使用 `私聊` 的方式在 QQ 对机器人发送 `/help` 以检查是否连接成功。