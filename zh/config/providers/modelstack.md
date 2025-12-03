# 接入到 ModelStack

[ModelStack](https://modelstack.app/) 是一个模型服务平台，提供了丰富的模型资源和API接口，支持多种模型格式和推理方式。**AstrBot 将会与 ModelStack 进行长期、深度的合作**，提供更好的模型服务体验。

AstrBot 支持接入 ModelStack 作为模型提供商，用户可以通过 ModelStack 来访问和使用各种 AI 模型服务。

![ModelStack](/source/images/modelstack/image.png)

## 配置步骤

### 获取 ModelStack API Key 密钥

在 ModelStack 注册并登录后，点击上方导航栏的「控制台」，点击「令牌管理」，然后点击「添加令牌」按钮，创建一个新的 API Key 密钥。

创建成功后，点击复制密钥按钮，复制生成的 API Key 密钥。

> [!TIP]
> 为了能够正常使用，你可能需要先支付 🤔。如果有任何支付问题，请立即联系 [i@modelstack.app](mailto:i@modelstack.app) 🚀。

### 选择模型

在上方导航栏的「模型广场」中选择需要使用的模型。

### 接入到 AstrBot

在 AstrBot 面板的「服务提供商」页面，点击「新增服务提供商」，选择「OpenAI」。（如果有 ModelStack 提供商，则选择「ModelStack」）。

- ID 命名为 `modelstack`（随意）
- API Base URL 填写 `https://modelstack.app/v1`
- API Key 填写上面获取的 API Key 密钥
- 模型名称填写上面选择的模型名称
- 点击「保存」按钮，完成创建。

### 应用模型

在 AstrBot 面板的「配置文件」页面，找到模型一节，将「默认聊天模型」修改为刚刚创建的 ModelStack 提供商，点击「保存」按钮，完成应用。
