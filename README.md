<div align="center">

# 🤖 AstrBot-Skill

**AstrBot SKILL · 让 AI 成为你的插件开发助手**

_✨ 结构化技术文档 + AGENT SKILL 定义 + MCP 服务器，赋能 AI 辅助开发 ✨_

[![GitHub Stars](https://img.shields.io/github/stars/EterUltimate/AstrBot-Skill?style=for-the-badge&logo=github&color=yellow)](https://github.com/EterUltimate/AstrBot-Skill)
[![GitHub Forks](https://img.shields.io/github/forks/EterUltimate/AstrBot-Skill?style=for-the-badge&logo=github&color=blue)](https://github.com/EterUltimate/AstrBot-Skill/fork)
[![QQ群](https://img.shields.io/badge/QQ群-1054962131-pink?style=for-the-badge&logo=tencent-qq&logoColor=white)](https://qm.qq.com/q/AstrBot)

</div>

---

## 🎯 这是什么？

AstrBot 的 **AGENT SKILL 仓库**，包含插件开发的结构化技术文档、Skill 定义和 MCP 服务器。

通过加载本仓库的 Skill，AI 可以：

- 🧠 理解 AstrBot 插件架构和 API
- 📝 生成符合规范的插件代码
- 🔧 提供准确的开发建议和调试帮助
- 📖 编写 AI 友好的技术文档
- 🔌 通过 MCP 协议与开发工具集成

---

## 🚀 快速开始

### 方式一：使用 Skill 文件

从 [Releases](https://github.com/EterUltimate/AstrBot-Skill/releases) 下载最新版本，将 Skill 文件内容提供给 AI 助手即可激活：

| Skill 文件 | 用途 |
|:----------:|:-----|
| [`skill-astrbot-dev/SKILL.md`](skill-astrbot-dev/SKILL.md) | **skill-astrbot-dev** — 插件开发参考（消息模型、平台适配器、Agent 系统等） |
| [`data/skills/docs4agent/SKILL.md`](data/skills/docs4agent/SKILL.md) | **docs4agent** — 技术文档写作规范 |

### 方式二：使用 MCP 服务器

```bash
# 安装依赖
cd mcp-astrbot
pip install -r requirements.txt

# 启动 MCP 服务器（stdio 模式）
python server.py
```

在支持 MCP 的客户端中配置：
```json
{
  "mcpServers": {
    "astrbot": {
      "command": "python",
      "args": ["/path/to/AstrBot-Skill/mcp-astrbot/server.py"]
    }
  }
}
```

### 示例

> 请阅读 `skill-astrbot-dev/SKILL.md`，然后帮我写一个 AstrBot 插件，实现：当收到消息时自动回复"你好！"

---

## 📚 项目结构

```
AstrBot-Skill/
├── skill-astrbot-dev/          # ⭐ 主 Skill（插件开发参考）
│   ├── SKILL.md                # Skill 定义文件
│   ├── references/             # 参考文档
│   │   ├── agent/              # Agent 系统
│   │   ├── design_standards/   # 设计标准
│   │   ├── messages/           # 消息模型
│   │   ├── plugin_config/      # 插件配置
│   │   └── platform_adapters/  # 平台适配器
│   └── scripts/                # 辅助脚本
├── mcp-astrbot/                # 🔌 MCP 服务器
│   ├── server.py               # MCP 服务器实现
│   ├── config.yaml             # MCP 配置
│   └── requirements.txt        # Python 依赖
├── data/skills/
│   └── docs4agent/             # ⭐ 文档写作规范 Skill
│       └── SKILL.md
├── docs/                       # 历史文档（VitePress，已弃用）
└── README.md
```

---

## 🔧 MCP 工具列表

| 工具名 | 描述 |
|:------:|:-----|
| `get_doc` | Fetch a specific document |
| `list_docs` | List all available documents |
| `search_docs` | Search documents by keyword |
| `get_hook_inventory` | Get the complete hook inventory |

---

## 🔗 相关链接

| 资源 | 链接 |
|:----:|:----:|
| 📖 官方文档（实时） | [AstrBot 主仓库 docs/](https://github.com/AstrBotDevs/AstrBot/tree/master/docs) |
| 🏠 AstrBot 主仓库 | [github.com/AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) |
| 📝 官方文档站 | [docs.astrbot.app](https://docs.astrbot.app/) |
| 🐛 问题反馈 | [GitHub Issues](https://github.com/AstrBotDevs/AstrBot/issues) |

---

## 🤝 加入社区

[官方交流群 **1054962131**](https://qm.qq.com/q/AstrBot)

---

## 📜 许可证

本项目为 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 的文档同步归档，仅供学习参考。

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star 支持一下！⭐**

Made with ❤️ by AstrBot Community

</div>
