# 安装 `astrbot-dev-skill`

`D:\程序\AstrBot-docs\docs` 这个目录本身就是 `astrbot-dev-skill` 的完整内容，不是只拷一个 `SKILL.md`。

安装时要把整个 `docs` 目录作为一个 Skill 一起提供给 AI，这样 AI 在读取 `SKILL.md` 后，才能继续访问它引用的其他文档，例如：

- `index.md`
- `design_standards/`
- `agent/`
- `plugin_config/`
- `messages/`
- `platform_adapters/`

## 正确目录结构

推荐把 `docs` 目录重命名为 `skill-astrbot-dev` 后再安装：

```text
skill-astrbot-dev/
├── SKILL.md
├── index.md
├── agent/
├── design_standards/
├── messages/
├── platform_adapters/
├── plugin_config/
└── ...
```

核心要求：

- `SKILL.md` 必须位于 Skill 根目录
- `SKILL.md` 引用到的其余文档必须保留原有相对路径
- 不要只复制 `SKILL.md`，否则 AI 无法继续读取剩余文档

## 方式一：安装到 AstrBot

适用于 AstrBot 管理面板上传 Skill。

1. 复制整个 `docs` 目录
2. 将复制出的目录重命名为 `skill-astrbot-dev`
3. 确认目录内保留完整文档结构
4. 将 `skill-astrbot-dev` 压缩为 `.zip`
5. 进入 AstrBot 管理面板 `插件 -> Skills`
6. 上传该压缩包

压缩包要求：

- 解压后顶层目录为 `skill-astrbot-dev/`
- `skill-astrbot-dev/` 下直接包含 `SKILL.md`
- 其他子目录和文档必须一并存在

## 方式二：安装到本地 Agent / Codex

适用于本地 Agent 直接从 skills 目录加载。

1. 找到本地 skills 根目录
2. 将整个 `docs` 目录复制进去
3. 将该目录命名为 `skill-astrbot-dev`

示例：

```text
<skills-root>/
└── skill-astrbot-dev/
    ├── SKILL.md
    ├── index.md
    ├── agent/
    ├── design_standards/
    ├── messages/
    ├── platform_adapters/
    ├── plugin_config/
    └── ...
```

如果当前使用的是 Codex，本机示例路径通常类似：

```text
C:\Users\<用户名>\.codex\skills\skill-astrbot-dev\
```

## 给 AI 的使用说明

安装后，AI 不应只读取 `SKILL.md`，还应按 `SKILL.md` 中的相对路径继续读取相关文档。

可以直接这样提示 AI：

```text
请使用 skill-astrbot-dev。先读取 SKILL.md，再按其中引用继续读取相关文档，不要只看一个文件。
```

或者：

```text
请加载 skill-astrbot-dev，并在分析插件开发问题时继续读取该 skill 目录下被引用的文档。
```

## 验证

安装完成后，应满足：

- Skill 列表中能看到 `skill-astrbot-dev`
- AI 能读取 `SKILL.md`
- AI 能继续访问 `index.md`、`agent/`、`plugin_config/` 等子文档

## 说明

- 此 Skill 的真实安装单位是整个 `docs` 目录
- `SKILL.md` 只是入口文件，不是完整内容
