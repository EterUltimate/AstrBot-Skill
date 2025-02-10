# 接入飞书

## 常见问题

如果发现 `加载平台适配器 lark 失败，原因：No module named 'lark_oapi'。请检查依赖库是否安装。提示：可以在 管理面板->控制台->安装Pip库 中安装依赖库。` 报错，说明没有安装 `lark_oapi` 库，请根据提示安装或者直接通过 pip 安装。

## 创建机器人

前往 [开发者后台](https://open.feishu.cn/app) ，创建企业自建应用。

![](../../source/images/lark/image.png)

添加应用能力——机器人。

![](../../source/images/lark/image-1.png)

点击凭证与基础信息，获取 app_id 和 app_secret。

![](../../source/images/lark/image-4.png)

## 配置 AstrBot

打开 AstrBot 管理面板->配置页->消息平台适配器->+，创建一个飞书（Lark）适配器。

![alt text](../../source/images/lark/image-12.png)

将刚刚复制的 app_id 和 app_secret 填入。以及飞书机器人的名字。

如果您正在用国际版飞书，请将 `domain` 设置为 `https://open.larksuite.com`。

然后点击右下角保存配置，等待重启成功。

## 设置回调和权限

点击事件与回调，使用长连接接收事件，点击保存。**如果上一步没有成功启动，那么这里将无法保存。**

![](../../source/images/lark/image-6.png)

点击添加事件，消息与群组，下拉找到 `接收消息`，添加。

![](../../source/images/lark/image-7.png)

点击开通以下权限。

![](../../source/images/lark/image-8.png)

再点击上面的`保存`按钮。

接下来，点击权限管理，点击开通权限，输入 `im:message:send,im:message,im:message:send_as_bot`。添加筛选到的权限。

再次输入 `im:resource:upload,im:resource` 开通上传图片相关的权限。

最终开通的权限如下图：

![alt text](../../source/images/lark/image-11.png)

## 创建版本

创建版本。

![](../../source/images/lark/image-2.png)

填写版本号，更新说明，可见范围后点击保存，确认发布。

## 拉入机器人到群组

进入飞书 APP（网页版飞书无法添加机器人），点进群聊，点击右上角按钮->群机器人->添加机器人。

搜索刚刚创建的机器人的名字。比如教程创建了 `AstrBot` 机器人：

![](../../source/images/lark/image-9.png)

## 🎉 大功告成

在群内发送一个 `/help` 指令，机器人将做出响应。

![](../../source/images/lark/image-13.png)