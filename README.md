
# AstrBot
_✨ 易上手的多平台 LLM 聊天机器人及开发框架（的官方文档） ✨_

[查看文档](https://docs.astrbot.app/) ｜ [问题提交](https://github.com/AstrBotDevs/AstrBot/issues)

[AstrBot](https://github.com/AstrBotDevs/AstrBot) 是一个松耦合、异步、支持多消息平台部署、具有易用的插件系统和完善的大语言模型（LLM）接入功能的聊天机器人及开发框架。

![image](https://github.com/user-attachments/assets/48f72a71-9456-4166-bbd2-f2a6c8cd740f)

## 自动同步（GitHub Actions）

工作流会周期性运行 `scripts/main.py`，并通过 LLM 生成/更新文档；LLM 相关配置均来自环境变量/Secrets（不会硬编码）。

- `GEMINI_API_KEY`（或 `OPENAI_API_KEY`）：API Key
- `BASE_URL`（或 `OPENAI_API_BASE`）：接口地址（例如公益站/代理的 URL）
- `MODEL_NAME`：模型名（例如 `gemini-3-flash-preview`）
- `LLM_API_STYLE`：`auto`（默认）/ `openai` / `gemini`
  - 使用 OpenAI-Compatible 站点时建议设为 `openai`
  - 使用 Google Gemini 原生接口时建议设为 `gemini`
- `GEMINI_API_VERSION`：Gemini 原生接口版本（默认 `v1beta`，仅 `LLM_API_STYLE=gemini` 时使用）

本地连通性测试：`python scripts/test_api.py`

