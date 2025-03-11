# 使用 Docker 部署 AstrBot

> [!WARNING]
> 通过 Docker 可以方便地将 AstrBot 部署到 Windows, Mac, Linux 上。
> 
> 以下教程默认您的环境已安装 Docker。如果没有安装，请参考 [Docker 官方文档](https://docs.docker.com/get-docker/) 进行安装。

> 如果网络环境在国内，可能无法正常拉取 Docker 镜像，请挂代理（需要额外在 Docker 设置中配置），或者使用国内镜像源。
> 镜像源可参考：[目前国内可用Docker镜像源汇总（截至2025年1月）](https://www.coderjia.cn/archives/dba3f94c-a021-468a-8ac6-e840f85867ea)
> 如果仍不会配置，请加群询问~


## 通过 Docker Compose 部署


首先，需要 Clone AstrBot 仓库到本地：

```bash
git clone https://github.com/Soulter/AstrBot
cd AstrBot
```

然后，运行 Compose：

```bash
sudo docker compose up -d
```

> Windows 下不需要加 sudo，下同

> [!TIP]
> 默认的 compose 文件没有映射宿主机的 docker.sock 文件，因此无法使用沙箱代码执行器。如果你需要使用沙箱代码执行器，请修改 `docker-compose.yml` 文件，添加在 volumes：
> ```yaml
> volumes:
>   - /var/run/docker.sock:/var/run/docker.sock
> ```

## 通过 Docker 部署

```bash
mkdir astrbot
sudo docker run -itd -p 6180-6200:6180-6200 -p 11451:11451 -v $PWD/data:/AstrBot/data -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro --name astrbot soulter/astrbot:latest
```

关于端口映射，如果您不想映射上面这么多端口，可以参考下表：

| Port    | Description | Type
| -------- | ------- | ------- |
| 6185 |  AstrBot WebUI `默认` 端口  | 需要 |
| 6195 | 企业微信 `默认` 端口    | 可选 |
| 6199 | OneBot(aiocqhttp) `默认` 端口    | 可选 |
| 6196    | QQ 官方 API(Webhook) HTTP callback server `默认` 端口   | 可选 |
| 11451    | Gewechat callback HTTP server `默认` 端口   | 可选 |


> Windows 下不需要加 sudo，下同
> Windows 同步 Host Time（需要WSL2）

```
-v \\wsl.localhost\(your-wsl-os)\etc\timezone:/etc/timezone:ro
-v \\wsl.localhost\(your-wsl-os)\etc\localtime:/etc/localtime:ro
```

通过以下命令查看 AstrBot 的日志：

```bash
sudo docker logs -f astrbot
```

> [!TIP]
> AstrBot 支持基于 Docker 的沙箱代码执行器。如果你需要使用沙箱代码执行器，请额外添加 `-v /var/run/docker.sock:/var/run/docker.sock` 参数。即:
> ```bash
> sudo docker run -itd -p 6180-6200:6180-6200 -p 11451:11451 -v $PWD/data:/AstrBot/data -v /var/run/docker.sock:/var/run/docker.sock -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro --name astrbot soulter/astrbot:latest
> ```


## 🎉 大功告成！

如果一切顺利，你会看到 AstrBot 打印出的日志。

如果没有报错，你会看到一条日志显示类似 `🌈 管理面板已启动，可访问` 并附带了几条链接。打开其中一个链接即可访问 AstrBot 管理面板。

> [!TIP]
> 由于 Docker 隔离了网络环境，所以不能使用 `localhost` 访问管理面板。
>
> 默认用户名和密码是 `astrbot` 和 `astrbot`。
>
> 如果部署在云服务器上，需要在相应厂商控制台里放行 `6180-6200` 和 `11451` 端口。


接下来，你需要部署任何一个消息平台，才能够实现在消息平台上使用 AstrBot。
