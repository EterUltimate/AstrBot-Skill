# 使用 Docker 部署 AstrBot

> [!WARNING]
> 通过 Docker 可以方便地将 AstrBot 部署到 Windows, Mac, Linux 上。
> 
> 以下教程默认您的环境已安装 Docker。如果没有安装，请参考 [Docker 官方文档](https://docs.docker.com/get-docker/) 进行安装。

## 通过 Docker Compose 部署

首先，需要 Clone AstrBot 仓库到本地：

```bash
git clone https://github.com/Soulter/AstrBot
cd AstrBot
```

然后，运行 Compose：

```bash
docker compose up
```

> [!TIP]
> 如果要在后台运行，请添加 `-d` 参数。建议第一次启动时不要加 `-d` 参数，以便查看日志。

## 通过 Docker 部署

```bash
mkdir astrbot
docker run -it --network=host -v $PWD/data:/AstrBot/data --name astrbot soulter/astrbot:latest
```

> [!TIP]
> 如果要在后台运行，请添加 `-d` 参数。建议第一次启动时不要加 `-d` 参数，以便查看日志。

## 🎉 大功告成！

如果一切顺利，你会看到 AstrBot 打印出的日志。

如果没有报错，你会看到一条日志显示类似 `🌈 管理面板已启动，可访问` 并附带了几条链接。打开其中一个链接即可访问 AstrBot 管理面板。

> [!TIP]
> 由于 Docker 隔离了网络环境，所以不能使用 `localhost` 访问管理面板。
>
> 默认用户名和密码是 `astrbot` 和 `astrbot`。


接下来，你需要部署任何一个消息平台，才能够实现在消息平台上使用 AstrBot。