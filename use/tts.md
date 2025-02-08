# 使用文字转语音

> 暂不支持 qq_official，参考 [AstrBot 适配情况](https://github.com/Soulter/AstrBot?tab=readme-ov-file#-%E6%B6%88%E6%81%AF%E5%B9%B3%E5%8F%B0%E6%94%AF%E6%8C%81%E6%83%85%E5%86%B5)

AstrBot 目前原生支持接入 OpenAI、Fish Audio TTS 模型，实现文字转语音。也支持适配了 OpenAI TTS API 的第三方 TTS 服务。如果你想使用 OpenAI TTS 服务，你需要一个 OpenAI API Key 或者使用中转服务（推荐 chatanywhere 或者 AiHubMix ）。

## 配置 OpenAI TTS

![](../source/images/tts/image.png)

添加，然后填写相关的配置项。

> [!TIP]
> 如果控制台提示未安装 `whisper` 库，请先点击管理面板->控制台页右上角的 `安装 Pip 库` 按钮安装此库。


## 配置 Fish Audio TTS

官网：https://fish-audio.cn/

Fish Audio 是一个小样本 TTS, 能快速生成 TTS 语音, 其团队包含了 GPT-Sovits 的创始人。 Fish Audio 还推出了线上 API。

首先，请登录官网注册账号，然后进入 [API Key](https://fish-audio.cn/zh-CN/go-api/api-keys/) 申请一个 API Key。

进入[账单](https://fish-audio.cn/zh-CN/go-api/billing/)，可以找到申请试用额度，点击申请即可，如果没有额度，可以充值。

在 AstrBot：

![](../source/images/tts/image-2.png)

然后填入你的 API Key。

> [!TIP]
> 如果控制台提示未安装 `ormsgpack` 库，请先点击管理面板->控制台页右上角的 `安装 Pip 库` 按钮安装此库。

## 启用 TTS

![](../source/images/tts/image-1.png)

在这里点击启用，然后保存配置。

如果启用了 TTS，在请求大模型得到文本回复之后，将会自动调用所启用的 TTS 服务。控制台会输出 `TTS 请求: xxx` 的 INFO 级别日志。