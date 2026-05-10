---
category: agent
---

# 人设管理 (Persona Sets)

插件侧通过 `self.context.persona_manager` 管理人设（Persona）。

## 数据模型

### Persona

```python
from astrbot.core.provider.entities import Persona

class Persona:
    id: str                     # 人设唯一 ID
    name: str                   # 人设名称
    prompt: str                 # 系统提示词
    system_prompt: str          # 系统提示词（同 prompt）
    folder_id: str | None       # 所属文件夹 ID
    sort_order: int             # 排序权重
    avatar: str | None          # 头像 URL
    description: str | None     # 人设描述
    begin_dialogs: list[str]    # 开场白列表
    model_config: dict | None   # 模型配置覆盖
    tools: list[str] | None     # 可用工具列表
    skills: list[str] | None    # 可用技能列表（仅 update 可修改）
```

### Personality

```python
from astrbot.core.provider.entities import Personality

class Personality:
    id: str
    name: str
    prompt: str
    begin_dialogs: list[str] | None
    model_config: dict | None
    avatar: str | None
    description: str | None
    folder_id: str | None
    sort_order: int
```

> `Persona` 是完整人设实体；`Personality` 是轻量视图，主要用于列表展示。

## PersonaManager 可用方法

### 读取

- `get_persona(persona_id: str) -> Persona | None`
- `get_all_persona() -> list[Personality]`
- `get_default_persona_v3() -> str | None`：获取默认人设 ID（从配置读取）。

### 创建

- `create_persona(name: str, prompt: str, begin_dialogs: list[str] | None = None, model_config: dict | None = None, avatar: str | None = None, description: str | None = None, folder_id: str | None = None, sort_order: int = 0) -> str`：返回新 ID。

### 更新

- `update_persona(persona_id: str, name: str | None = None, prompt: str | None = None, begin_dialogs: list[str] | None = None, model_config: dict | None = None, avatar: str | None = None, description: str | None = None, tools: list[str] | None = None, skills: list[str] | None = None) -> None`

### 删除

- `delete_persona(persona_id: str) -> None`

### 文件夹管理

- `get_persona_folders() -> list[dict]`
- `create_persona_folder(name: str) -> str`
- `delete_persona_folder(folder_id: str) -> None`

## 示例

```python
persona_mgr = self.context.persona_manager

# 创建人设
pid = await persona_mgr.create_persona(
    name="助手A",
    prompt="你是一个有帮助的助手。",
    begin_dialogs=["你好！我是助手A。"],
    folder_id="folder_xxx",
    sort_order=10,
)

# 更新人设（含 skills）
await persona_mgr.update_persona(
    persona_id=pid,
    name="助手A-V2",
    skills=["tool_search", "web_browse"],
)

# 获取所有人设（返回 Personality 列表）
all_personas = await persona_mgr.get_all_persona()

# 获取完整人设对象
persona = await persona_mgr.get_persona(pid)
```

## 注意事项

- `create_persona` 的 `folder_id` 和 `sort_order` 可选；`update_persona` 不支持修改 `folder_id`/`sort_order`。
- `update_persona` 支持 `tools` 和 `skills` 字段，`create_persona` 不支持。
- `tools`：工具名列表，控制人设可调用的函数工具；`skills`：技能名列表，语义类似但用于插件级别的技能管理。
- 删除文件夹会级联处理其中的人设（具体行为视实现而定，建议先移出人设再删文件夹）。
