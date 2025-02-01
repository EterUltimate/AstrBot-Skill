## 接入 LMStudio 使用 DeepSeek-R1 等模型

LMStudio 允许在本地电脑上部署模型（需要电脑硬件配置符合要求）

### 下载并安装 LMStudio

https://lmstudio.ai/download

### 下载并运行模型

https://lmstudio.ai/models

跟随 LMStudio 下载并运行想要的模型，如 deepseek-r1-qwen-7b:

```bash
lms get deepseek-r1-qwen-7b
```

### 配置 AstrBot

在 AstrBot 上：

点击 配置->服务提供商配置->加号->openai

API Base URL 填写 `http://localhost:1234/v1`

模型名填写上一步选好的

保存配置即可。

> 输入 /provider 查看 AstrBot 配置的模型