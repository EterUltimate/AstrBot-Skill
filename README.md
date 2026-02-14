<div align="center">

# 🤖 AstrBot-docs

**AstrBot  SKILL · 让 AI 成为你的插件开发助手**

_✨ 结构化技术文档 + AGENT SKILL 定义，赋能 AI 辅助开发 ✨_

[![GitHub Stars](https://img.shields.io/github/stars/xunxiing/AstrBot-docs?style=for-the-badge&logo=github&color=yellow)](https://github.com/xunxiing/AstrBot-docs)
[![GitHub Forks](https://img.shields.io/github/forks/xunxiing/AstrBot-docs?style=for-the-badge&logo=github&color=blue)](https://github.com/xunxiing/AstrBot-docs/fork)
[![QQ群](https://img.shields.io/badge/QQ群-1054962131-pink?style=for-the-badge&logo=tencent-qq&logoColor=white)](https://qm.qq.com/q/AstrBot)

</div>

---

## 🎯 这是什么？

这是一个 **AGENT SKILL 仓库**，包含 AstrBot 插件开发的结构化技术文档和 Skill 定义文件。

**AGENT SKILL** 是一种让 AI 助手（如 Claude、ChatGPT 等）获得特定领域知识的技术。通过加载本仓库的 Skill，AI 可以：

- 🧠 理解 AstrBot 插件架构和 API
- 📝 生成符合规范的插件代码
- 🔧 提供准确的开发建议和调试帮助
- 📖 编写 AI 友好的技术文档

---

## 🚀 快速开始

### 在 AI 助手中使用

将 `docs/skill.md` 或 `data/skills/docs4agent/SKILL.md` 的内容提供给 AI 助手，即可激活对应 Skill：

| Skill 文件 | 用途 |
|:----------:|:-----|
| [`docs/skill.md`](docs/skill.md) | **skill-astrbot-dev** - AstrBot 插件开发参考，包含消息模型、平台适配器、Agent 系统等 |
| [`data/skills/docs4agent/SKILL.md`](data/skills/docs4agent/SKILL.md) | **docs4agent** - 极简主义、代码优先、AI 友好的技术文档写作规范 |

### 示例：让 AI 帮你写插件

```
请阅读 docs/skill.md，然后帮我写一个 AstrBot 插件，
实现：当收到消息时，自动回复"你好！"
```

---

## 📚 文档结构

```
docs/
├── skill.md              # ⭐ skill-astrbot-dev 定义文件
├── index.md              # 文档索引入口
├── design_standards/     # 核心概念、架构、最佳实践
├── agent/                # Agent 系统（工具/子智能体/沙盒/定时任务）
├── messages/             # 消息模型、事件、组件
├── plugin_config/        # 插件配置、装饰器、生命周期、Hooks
├── platform_adapters/    # 平台适配器接口
├── Storage & Utils/      # 存储与工具类
└── snapshots/            # 版本快照（v4.11.2, v4.12.x...）

data/skills/
└── docs4agent/
    └── SKILL.md          # ⭐ docs4agent 定义文件
```

---

## 🔗 相关链接

| 资源 | 链接 |
|:----:|:----:|
| 📖 在线预览 | [GitHub Pages](https://xunxiing.github.io/AstrBot-docs/) |
| 🏠 AstrBot 主仓库 | [github.com/AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot) |
| 📝 官方文档 | [docs.astrbot.app](https://docs.astrbot.app/) |
| 🐛 问题反馈 | [GitHub Issues](https://github.com/AstrBotDevs/AstrBot/issues) |

---

## 🤝 加入社区

<table>
<tr>
<td align="center">
<a href="https://qm.qq.com/q/AstrBot">
<img src="https://img.shields.io/badge/QQ群-1054962131-12B7F5?style=for-the-badge&logo=tencent-qq&logoColor=white" alt="QQ群"/>
<br/>
<strong>官方交流群</strong>
</a>
</td>
</tr>
</table>

欢迎加入官方 QQ 群 **1054962131**，获取技术支持、交流开发经验！

### 本地测试

```bash
python scripts/test_api.py
```

---

## 📜 许可证

本项目基于 AstrBot 官方仓库进行同步归档，仅供学习参考使用。

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star 支持一下！⭐**

Made with ❤️ by AstrBot Community

</div>
