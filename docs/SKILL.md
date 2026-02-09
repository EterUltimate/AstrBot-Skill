---
name: skill-astrbot-dev
description: Reference + workflow notes for AstrBot plugin development (messages, platform adapters, plugin config, agent system).
metadata:
  short-description: AstrBot dev reference
---

# skill-astrbot-dev

This skill is the source-of-truth index for AstrBot developer docs in this repo (`docs/`).

Goal: when this skill is selected, immediately ground on the minimum required docs + code entrypoints,
avoid duplicated reading, and always prefer code as the final authority.

## When to use

Use this skill when you ask for help with:
- AstrBot plugin structure, decorators/hooks, lifecycle, schema, sessions
- Message model/event flow and message-chain conversion
- Platform adapter interface and message conversion patterns
- Agent topics (tools/providers/personas/subagents/sandbox/cron/context compression)

## Mandatory workflow (use this every time)

1. Start from a single entrypoint (avoid broad loading):
   - Site index: `docs/index.md`
   - Core concepts: `docs/design_standards/core_concepts.md`
2. Pick one topic folder and stay focused:
   - Agent system: `docs/agent/`
   - Plugin config: `docs/plugin_config/`
   - Messages: `docs/messages/`
   - Platform adapters: `docs/platform_adapters/`
3. If the user targets a specific AstrBot version, cross-check:
   - `docs/snapshots/<version>/`
4. If docs and code disagree, treat code as truth:
   - Core code lives under `astrbotcore/astrbot/core/` (read only the needed files).

## Hooks: avoid missing / outdated references

There are two different "hook" layers you must not mix up:

- Plugin event hooks (decorators): `docs/plugin_config/hooks.md`
- Agent runner hooks (`BaseAgentRunHooks`): `docs/agent/hooks.md`

If you need a complete hook inventory (because context may be truncated), generate it locally:

```powershell
python scripts/generate_hook_inventory.py
```

This writes to `docs/.tmp/hook_inventory/` (gitignored). Use it as a scratchpad for writing/updating docs;
do not reference `.tmp` paths as public documentation URLs.

## High-signal code entrypoints (open only when needed)

- Event hooks registration + signatures: `astrbotcore/astrbot/core/star/register/star_handler.py`
- Event types: `astrbotcore/astrbot/core/star/star_handler.py`
- Agent runners + hook call order: `astrbotcore/astrbot/core/agent/runners/`
- Agent hook interface: `astrbotcore/astrbot/core/agent/hooks.py`
- Main agent build (sandbox/cron/tools): `astrbotcore/astrbot/core/astr_main_agent.py`
- Skills system (AstrBot runtime skills): `astrbotcore/astrbot/core/skills/skill_manager.py`
- Subagents config loading: `astrbotcore/astrbot/core/subagent_orchestrator.py`
