#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AstrBot MCP Server
Provides tool interfaces for AstrBot plugin development.
"""

import json
import asyncio
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent

# MCP server instance
app = Server("astrbot-mcp")

# Document index
DOCS_INDEX = {
    "agent": {
        "agent-runner": "Agent Runner overview and configuration",
        "agent-related-hooks": "Agent-related hooks",
        "conversation": "Conversation management",
        "context-compression": "Context compression",
        "cron": "Scheduled tasks (cron)",
        "Invoke-llm": "Invoking LLM",
        "persona-resolution": "Persona resolution",
        "persona-sets": "Persona sets",
        "registe tools": "Tool registration",
        "sandbox": "Sandbox environment",
        "subagents": "Sub-agents",
    },
    "design_standards": {
        "architecture_overview": "Architecture overview",
        "best_practices": "Best practices",
        "context_usage": "Context usage",
        "core_concepts": "Core concepts",
        "event_flow": "Event flow",
        "sandbox": "Sandbox design",
        "visual_utils": "Visual utilities",
    },
    "messages": {
        "components": "Message components",
        "events": "Message events",
        "model": "Message model",
        "umo": "UMO model",
    },
    "plugin_config": {
        "command_management": "Command management",
        "decorators": "Decorators",
        "file_config": "File configuration",
        "hooks": "Hooks",
        "lifecycle": "Lifecycle",
        "schema": "Configuration schema",
        "session_control": "Session control",
    },
    "platform_adapters": {
        "adapter_interface": "Adapter interface",
        "message_conversion": "Message conversion",
        "telegram_media_group": "Telegram media group",
    },
}


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="get_doc",
            description="Fetch AstrBot development document content",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": [
                            "agent",
                            "design_standards",
                            "messages",
                            "plugin_config",
                            "platform_adapters",
                        ],
                        "description": "Document category",
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "Document name (without .md suffix)",
                    },
                },
                "required": ["category", "doc_name"],
            },
        ),
        Tool(
            name="list_docs",
            description="List all available documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": [
                            "agent",
                            "design_standards",
                            "messages",
                            "plugin_config",
                            "platform_adapters",
                        ],
                        "description": "Document category (optional; lists all if omitted)",
                    }
                },
            },
        ),
        Tool(
            name="search_docs",
            description="Search document content by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword",
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_hook_inventory",
            description="Get the complete hook inventory",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Dispatch tool calls."""
    if name == "get_doc":
        return await get_doc(arguments["category"], arguments["doc_name"])
    elif name == "list_docs":
        category = arguments.get("category")
        return await list_all_docs(category)
    elif name == "search_docs":
        return await search_docs(arguments["query"])
    elif name == "get_hook_inventory":
        return await get_hook_inventory()
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def get_doc(category: str, doc_name: str) -> List[TextContent]:
    """Fetch a specific document."""
    import os

    base_path = os.path.join(
        os.path.dirname(__file__), "..", "skill-astrbot-dev", "references"
    )
    file_path = os.path.join(base_path, category, f"{doc_name}.md")

    if not os.path.exists(file_path):
        return [
            TextContent(
                type="text", text=f"Document not found: {category}/{doc_name}.md"
            )
        ]

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return [TextContent(type="text", text=content)]


async def list_all_docs(category: Optional[str] = None) -> List[TextContent]:
    """List all available documents, optionally filtered by category."""
    if category:
        if category not in DOCS_INDEX:
            return [TextContent(type="text", text=f"Unknown category: {category}")]

        docs = DOCS_INDEX[category]
        result = f"## {category}\n\n"
        for doc_id, desc in docs.items():
            result += f"- `{doc_id}`: {desc}\n"

        return [TextContent(type="text", text=result)]
    else:
        result = "# AstrBot Development Docs Index\n\n"
        for cat, docs in DOCS_INDEX.items():
            result += f"## {cat}\n\n"
            for doc_id, desc in docs.items():
                result += f"- `{doc_id}`: {desc}\n"
            result += "\n"

        return [TextContent(type="text", text=result)]


async def search_docs(query: str) -> List[TextContent]:
    """Search documents for a keyword and return matching context."""
    import os

    base_path = os.path.join(
        os.path.dirname(__file__), "..", "skill-astrbot-dev", "references"
    )
    results = []

    for category in DOCS_INDEX.keys():
        cat_path = os.path.join(base_path, category)
        if not os.path.exists(cat_path):
            continue

        for filename in os.listdir(cat_path):
            if not filename.endswith(".md"):
                continue

            file_path = os.path.join(cat_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if query.lower() in content.lower():
                lines = content.split("\n")
                matched_lines = []
                for i, line in enumerate(lines):
                    if query.lower() in line.lower():
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        matched_lines.extend(lines[start:end])
                        matched_lines.append("---")

                if matched_lines:
                    doc_name = filename[:-3]
                    results.append(
                        f"### {category}/{doc_name}\n"
                        + "\n".join(matched_lines[:20])
                    )

    if not results:
        return [
            TextContent(
                type="text", text=f"No documents found matching '{query}'"
            )
        ]

    return [TextContent(type="text", text="\n\n".join(results[:5]))]


async def get_hook_inventory() -> List[TextContent]:
    """Return the pre-generated hook inventory."""
    import os

    hook_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "skill-astrbot-dev",
        ".tmp",
        "hook_inventory",
    )

    if os.path.exists(hook_path):
        result = "# AstrBot Hook Inventory\n\n"
        for filename in sorted(os.listdir(hook_path)):
            if filename.endswith(".md"):
                with open(
                    os.path.join(hook_path, filename), "r", encoding="utf-8"
                ) as f:
                    result += f.read() + "\n\n"
        return [TextContent(type="text", text=result)]
    else:
        return [
            TextContent(
                type="text",
                text="Hook inventory not generated. Run `python scripts/generate_hook_inventory.py` to generate it.",
            )
        ]


async def main():
    """Entry point."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, write_stream, app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
