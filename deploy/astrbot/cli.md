# 通过源码部署 AstrBot

> [!WARNING]
> 你正在直接通过源码来部署本项目，该教程需要您具有一定的技术基础。
>
> 以下教程默认您的设备上已经安装 Python，并且版本 `>=3.10`


## 下载源码

如果你的电脑上安装了 `git`，你可以通过以下命令来下载源码：

```bash
git clone http://github.com/Soulter/AstrBot
cd AstrBot
```

如果你没有安装 `git`，你可以直接在 [GitHub](https://github.com/Soulter/AstrBot/releases/latest) 上下载 `Source code (zip)` 并解压到您的电脑。

## 运行源码

在 AstrBot 源码目录下，使用终端运行以下命令：

```bash
python3 -m venv ./venv
source venv/bin/activate
```

以上步骤会创建一个虚拟环境并激活（以免打乱你电脑本地的 Python 环境），并使用清华大学的镜像源来安装 AstrBot 的依赖。依赖的安装需要花费一些时间。

接下来，通过以下命令安装依赖文件：

```bash
python3 -m pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

> [!TIP]
> 推荐使用更快的 uv 工具来安装依赖文件（平均快 10-100 倍）：
> ```bash
> python3 -m pip install uv
> python3 -m uv pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
> ```

然后运行 AstrBot

```bash
python3 main.py
```

## 🎉 大功告成！

如果一切顺利，你会看到 AstrBot 打印出的日志。

如果没有报错，你会看到一条日志显示类似 `🌈 管理面板已启动，可访问` 并附带了几条链接。打开其中一个链接即可访问 AstrBot 管理面板。链接是 `http://localhost:6185`。

> [!TIP]
> 如果你正在服务器上部署 AstrBot，需要将 `localhost` 替换为你的服务器 IP 地址。
>
> 默认用户名和密码是 `astrbot` 和 `astrbot`。


接下来，你需要部署任何一个消息平台，才能够实现在消息平台上使用 AstrBot。
