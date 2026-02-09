---
category: agent
---

# Skills（本地技能指令集）

AstrBot 的 Skills 用于把一组“本地指令 + 参考文件”打包成可复用的技能单元（以 `SKILL.md` 为入口），供 Agent 在对话中按需选择/触发。

> 注意：这里的 “skills” 指 AstrBot 运行时的 skill 系统，不等同于本仓库 `docs/SKILL.md`（后者是给文档/RAG 的 skill 入口文件）。

## Skill 的基本形态

- 一个 skill 是一个目录，目录内必须包含 `SKILL.md`
- `SKILL.md` 通常包含 frontmatter（name/description）与使用规范
- Skill 可以启用/禁用，并以配置文件 `skills.json` 管理

## SkillManager（运行时）

核心实现入口：

- `astrbotcore/astrbot/core/skills/skill_manager.py`

你会在这里看到：

- skill 扫描与描述提取（frontmatter `description`）
- skill 配置文件 `skills.json` 的读写
- sandbox 模式下的 skill 路径映射（将本地路径映射为 sandbox 内路径）

## 与 Sandbox 的关系

当启用 sandbox runtime 时，技能包可能会被同步到沙盒环境（用于在沙盒内执行/引用相关文件）。

相关实现：

- `astrbotcore/astrbot/core/computer/computer_client.py`（`_sync_skills_to_sandbox`）

## 最佳实践（写 skill 时）

- 只在 `SKILL.md` 放“必读规则”和“最短流程”；避免和站点 `index.md` 重复
- 明确入口文件路径与优先级（从哪个文档/源码开始读）
- 避免把大量内容堆进同一个 skill：把长文拆成可跳转的页面/文件，让 Agent 只加载必要部分
