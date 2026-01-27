
# AstrBot-docs
_✨ 易上手的多平台 LLM 聊天机器人及开发框架（的文档镜像/快照） ✨_

[在线预览（GitHub Pages）](https://xunxiing.github.io/AstrBot-docs/) ｜ [AstrBot 主仓库（致敬）](https://github.com/AstrBotDevs/AstrBot) ｜ [官方文档](https://docs.astrbot.app/) ｜ [问题提交](https://github.com/AstrBotDevs/AstrBot/issues)

本仓库用于自动同步/归档 AstrBot 的开发文档快照，并将其发布为可浏览的静态站点。

![image](https://github.com/user-attachments/assets/48f72a71-9456-4166-bbd2-f2a6c8cd740f)

## 自动同步（GitHub Actions）

工作流会周期性运行 `scripts/main.py`，并通过 LLM 生成/更新文档；LLM 相关配置均来自环境变量/Secrets（不会硬编码）。

- `GEMINI_API_KEY`（或 `OPENAI_API_KEY`）：API Key
- `BASE_URL`（或 `OPENAI_API_BASE`）：接口地址（例如公益站/代理的 URL）
- `MODEL_NAME`：模型名（例如 `gemini-3-flash-preview`）
- `LLM_MAX_TOKENS`：文档 AI 生成的最大输出 token 数（默认 `12000`）。若出现 JSON 解析失败（常见于输出被截断），可尝试增大该值。
- `LLM_API_STYLE`：`auto`（默认）/ `openai` / `gemini`
  - 使用 OpenAI-Compatible 站点时建议设为 `openai`
  - 使用 Google Gemini 原生接口时建议设为 `gemini`
- `GEMINI_API_VERSION`：Gemini 原生接口版本（默认 `v1beta`，仅 `LLM_API_STYLE=gemini` 时使用）
- `SHOW_BASE_URL_IN_LOGS`：是否在日志中输出 `BASE_URL`（默认 `0`，建议保持隐藏；本地排查时可设为 `1`）

本地连通性测试：`python scripts/test_api.py`
