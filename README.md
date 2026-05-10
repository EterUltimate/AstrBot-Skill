<div align="center">

# 🤖 AstrBot-Skill

**AstrBot SKILL · 让 AI 成为你的插件开发助手**

_✨ 结构化技术文档 + AGENT SKILL 定义，赋能 AI 辅助开发 ✨_

[![GitHub Stars](https://img.shields.io/github/stars/EterUltimate/AstrBot-Skill?style=for-the-badge&logo=github&color=yellow)](https://github.com/EterUltimate/AstrBot-Skill)
[![GitHub Forks](https://img.shields.io/github/forks/EterUltimate/AstrBot-Skill?style=for-the-badge&logo=github&color=blue)](https://github.com/EterUltimate/AstrBot-Skill/fork)
[![QQ群](https://img.shields.io/badge/QQ群-1054962131-pink?style=for-the-badge&logo=tencent-qq&logoColor=white)](https://qm.qq.com/q/AstrBot)

</div>

---

## 🎯 这是什么？

AstrBot 的 **AGENT SKILL 仓库**，包含插件开发的结构化技术文档和 Skill 定义。

通过加载本仓库的 Skill，AI 可以：

- 🧠 理解 AstrBot 插件架构和 API
- 📝 生成符合规范的插件代码
- 🔧 提供准确的开发建议和调试帮助
- 📖 编写 AI 友好的技术文档

> 📌 **MCP 服务器已拆分到独立仓库**：[EterUltimate/astrbot-mcp](https://github.com/EterUltimate/astrbot-mcp)

---

## 🚀 快速开始

从 [Releases](https://github.com/EterUltimate/AstrBot-Skill/releases) 下载最新版本，将 Skill 文件内容提供给 AI 助手即可激活：

| Skill 文件 | 用途 |
|:----------:|:-----|
| [`skill-astrbot-dev/SKILL.md`](skill-astrbot-dev/SKILL.md) | **skill-astrbot-dev** — 插件开发参考（消息模型、平台适配器、Agent 系统等） |

### 示例

> 请阅读 `skill-astrbot-dev/SKILL.md`，然后帮我写一个 AstrBot 插件，实现：当收到消息时自动回复"你好！"

---

## 📚 项目结构

```
AstrBot-Skill/
├── skill-astrbot-dev/          # ⭐ 主 Skill（插件开发参考）
│   ├── SKILL.md                # Skill 定义文件
│   └── references/             # 参考文档
│       ├── agent/              # Agent 系统（工具、对话、人设、子代理等）
│       ├── design_standards/   # 设计标准
│       ├── messages/           # 消息模型
│       ├── plugin_config/      # 插件配置（装饰器、钩子、Schema、i18n、页面等）
│       └── platform_adapters/  # 平台适配器
├── scripts/                    # 辅助脚本（Hook 清单生成等）
└── README.md
```

---

## 🔗 相关链接

| 资源 | 链接 |
|:----:|:----:|
| 🔌 MCP 服务器 | [EterUltimate/astrbot-mcp](https://github.com/EterUltimate/astrbot-mcp) |
| 📖 官方文档（实时） | [AstrBot 主仓库 docs/](https://github.com/AstrBotDevs/AstrBot/tree/master/docs) |
| 🏠 AstrBot 主仓库 | [github.com/AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) |
| 📝 官方文档站 | [docs.astrbot.app](https://docs.astrbot.app/) |
| 🐛 问题反馈 | [GitHub Issues](https://github.com/EterUltimate/AstrBot-Skill/issues) |

---

## 🤝 加入社区

[官方交流群 **1054962131**](https://qm.qq.com/q/AstrBot)

---

## 📜 许可证

MIT License

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star 支持一下！⭐**

Made with ❤️ by AstrBot Community

</div>
