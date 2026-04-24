#!/usr/bin/env python3
"""
AstrBot MCP Server
提供 AstrBot 插件开发相关的工具接口
"""

import json
import asyncio
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent

# 创建 MCP 服务器
app = Server("astrbot-mcp")

# 文档索引
DOCS_INDEX = {
    "agent": {
        "agent-runner": "Agent Runner 概述与配置",
        "agent-related-hooks": "Agent 相关 Hooks",
        "conversation": "对话管理",
        "context-compression": "上下文压缩",
        "cron": "定时任务",
        "Invoke-llm": "调用 LLM",
        "persona-resolution": "人格解析",
        "persona-sets": "人格集合",
        "registe tools": "工具注册",
        "sandbox": "沙盒环境",
        "subagents": "子智能体",
    },
    "design_standards": {
        "architecture_overview": "架构概览",
        "best_practices": "最佳实践",
        "context_usage": "上下文使用",
        "core_concepts": "核心概念",
        "event_flow": "事件流",
        "sandbox": "沙盒设计",
        "visual_utils": "可视化工具",
    },
    "messages": {
        "components": "消息组件",
        "events": "消息事件",
        "model": "消息模型",
        "umo": "UMO 模型",
    },
    "plugin_config": {
        "command_management": "命令管理",
        "decorators": "装饰器",
        "file_config": "文件配置",
        "hooks": "Hooks",
        "lifecycle": "生命周期",
        "schema": "配置 Schema",
        "session_control": "会话控制",
    },
    "platform_adapters": {
        "adapter_interface": "适配器接口",
        "message_conversion": "消息转换",
        "telegram_media_group": "Telegram 媒体组",
    },
}

@app.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="get_doc",
            description="获取 AstrBot 开发文档内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["agent", "design_standards", "messages", "plugin_config", "platform_adapters"],
                        "description": "文档类别"
                    },
                    "doc_name": {
                        "type": "string",
                        "description": "文档名称（不含 .md 后缀）"
                    }
                },
                "required": ["category", "doc_name"]
            }
        ),
        Tool(
            name="list_docs",
            description="列出所有可用文档",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["agent", "design_standards", "messages", "plugin_config", "platform_adapters"],
                        "description": "文档类别（可选，不填则列出所有）"
                    }
                }
            }
        ),
        Tool(
            name="search_docs",
            description="搜索文档内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_hook_inventory",
            description="获取完整的 Hook 清单",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """调用工具"""
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
        return [TextContent(type="text", text=f"未知工具: {name}")]

async def get_doc(category: str, doc_name: str) -> List[TextContent]:
    """获取指定文档内容"""
    import os
    
    # 构建文件路径
    base_path = os.path.join(os.path.dirname(__file__), "..", "skill-astrbot-dev", "references")
    file_path = os.path.join(base_path, category, f"{doc_name}.md")
    
    if not os.path.exists(file_path):
        return [TextContent(type="text", text=f"文档不存在: {category}/{doc_name}.md")]
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return [TextContent(type="text", text=content)]

async def list_all_docs(category: Optional[str] = None) -> List[TextContent]:
    """列出所有可用文档"""
    if category:
        if category not in DOCS_INDEX:
            return [TextContent(type="text", text=f"未知类别: {category}")]
        
        docs = DOCS_INDEX[category]
        result = f"## {category} 类别文档\n\n"
        for doc_id, desc in docs.items():
            result += f"- `{doc_id}`: {desc}\n"
        
        return [TextContent(type="text", text=result)]
    else:
        result = "# AstrBot 开发文档索引\n\n"
        for cat, docs in DOCS_INDEX.items():
            result += f"## {cat}\n\n"
            for doc_id, desc in docs.items():
                result += f"- `{doc_id}`: {desc}\n"
            result += "\n"
        
        return [TextContent(type="text", text=result)]

async def search_docs(query: str) -> List[TextContent]:
    """搜索文档内容"""
    import os
    import re
    
    base_path = os.path.join(os.path.dirname(__file__), "..", "skill-astrbot-dev", "references")
    results = []
    
    # 遍历所有文档
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
            
            # 搜索匹配
            if query.lower() in content.lower():
                # 提取匹配的上下文
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
                    results.append(f"### {category}/{doc_name}\n" + "\n".join(matched_lines[:20]))
    
    if not results:
        return [TextContent(type="text", text=f"未找到包含 '{query}' 的文档")]
    
    return [TextContent(type="text", text="\n\n".join(results[:5]))]

async def get_hook_inventory() -> List[TextContent]:
    """获取 Hook 清单"""
    import os
    
    # 尝试读取预生成的 hook 清单
    hook_path = os.path.join(os.path.dirname(__file__), "..", "skill-astrbot-dev", ".tmp", "hook_inventory")
    
    if os.path.exists(hook_path):
        result = "# AstrBot Hook 清单\n\n"
        for filename in sorted(os.listdir(hook_path)):
            if filename.endswith(".md"):
                with open(os.path.join(hook_path, filename), "r", encoding="utf-8") as f:
                    result += f.read() + "\n\n"
        return [TextContent(type="text", text=result)]
    else:
        return [TextContent(type="text", text="Hook 清单未生成。请运行 `python scripts/generate_hook_inventory.py` 生成。")]

async def main():
    """主函数"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
