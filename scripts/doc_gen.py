import os
import json
import re
import time
from typing import List, Dict, Optional
from datetime import datetime
from config import config
from llm_client import HttpError, generate_text

class DocGenerator:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY (or OPENAI_API_KEY) is not set in environment variables.")
        self.__api_key = config.GEMINI_API_KEY
        self.base_url = config.BASE_URL.rstrip('/')
        self.model_name = config.MODEL_NAME
        self.api_style = config.LLM_API_STYLE
        self.docs_root = "docs"
        self.show_base_url_in_logs = config.SHOW_BASE_URL_IN_LOGS
        self.categories = [
            "ai_integration",
            "storage",
            "messages",
            "plugin_config",
            "design_standards",
            "platform_adapters"
        ]
        self.default_category = "design_standards"

    def _get_base_context(self) -> str:
        """递归读取 docs/ 下的所有分类文件夹（排除 snapshots/）下的 md 文件作为上下文。
        确保 core_concepts.md 放在最开头。
        """
        context = []
        if not os.path.exists(self.docs_root):
            return ""

        # 1. 优先读取核心概念文档
        core_concept_path = os.path.join(self.docs_root, "design_standards", "core_concepts.md")
        if os.path.exists(core_concept_path):
            rel_path = os.path.relpath(core_concept_path, self.docs_root)
            with open(core_concept_path, "r", encoding="utf-8") as f:
                context.append(f"--- Doc: {rel_path} (CORE) ---\n{f.read()}")

        # 2. 递归读取其他文档
        for root, dirs, files in os.walk(self.docs_root):
            # 排除 snapshots 目录
            if "snapshots" in root.split(os.sep):
                continue
            
            for filename in sorted(files):
                if filename.endswith(".md"):
                    full_path = os.path.join(root, filename)
                    # 跳过已经添加的核心概念文档
                    if os.path.normpath(full_path) == os.path.normpath(core_concept_path):
                        continue
                        
                    rel_path = os.path.relpath(full_path, self.docs_root)
                    with open(full_path, "r", encoding="utf-8") as f:
                        context.append(f"--- Doc: {rel_path} ---\n{f.read()}")
        
        return "\n\n".join(context)

    def _handle_exception(self, e: Exception, context: str):
        """统一处理异常"""
        error_msg = self._mask_sensitive(str(e))
        print(f"{context} 出错: {error_msg}")
        
        if isinstance(e, HttpError):
            print(f"API 诊断: 状态码={e.status_code}, 消息={error_msg}")
            if e.status_code == 401:
                print("诊断建议: API Key 无效，请检查环境变量 GEMINI_API_KEY。")
            elif e.status_code == 403:
                print("诊断建议: 权限不足或被封禁，请检查 API Key 权限或 IP 区域。")
            elif e.status_code == 429:
                print("诊断建议: 触发频率限制，请稍后再试或更换 API Key。")
            elif e.status_code >= 500:
                print("诊断建议: 上游服务端错误，请稍后重试。")
        
        print("提示: 如果遇到连通性问题，请尝试运行 `python scripts/test_api.py` 进行故障排查。")

    def _mask_sensitive(self, text: str) -> str:
        """脱敏日志中的 API Key"""
        if not self.__api_key:
            return text
        return text.replace(self.__api_key, "***")

    def _call_gemini(self, prompt: str, system_instruction: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """使用 curl 调用 Gemini/OpenAI-Compatible API"""
        
        # 打印请求信息 (脱敏)
        print(f"发起请求: model={self.model_name}")
        if self.show_base_url_in_logs:
            print(f"  - Base URL: {self._mask_sensitive(self.base_url)}")
        else:
            print("  - Base URL: (hidden)")
        print(f"  - API Style: {self.api_style}")
        print(f"  - Temperature: {temperature}")

        max_retries = 3
        for attempt in range(max_retries):
            try:
                return generate_text(
                    api_key=self.__api_key,
                    base_url=self.base_url,
                    model_name=self.model_name,
                    prompt=prompt,
                    system_instruction=system_instruction,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    api_version=config.GEMINI_API_VERSION,
                    api_style=self.api_style,
                    timeout_seconds=600,
                )
            
            except HttpError as e:
                if e.status_code in [403, 429] and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"收到 API 错误 {e.status_code}，正在进行第 {attempt + 1} 次重试，等待 {wait_time} 秒...")
                    time.sleep(wait_time)
                    continue
                raise e
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"请求发生异常: {self._mask_sensitive(str(e))}，正在进行第 {attempt + 1} 次重试...")
                    time.sleep(wait_time)
                    continue
                raise e

    def _extract_json(self, text: str) -> Dict:
        """从 Gemini 的 Markdown 响应中提取 JSON 字符串"""
        # 尝试匹配 ```json ... ```
        json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 如果没有 Markdown 块，尝试寻找第一个 { 和最后一个 }
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                json_str = text[start:end+1]
            else:
                json_str = text
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # 极端情况下的安全保障
            masked_text = self._mask_sensitive(text)
            print(f"Failed to decode JSON from text: {masked_text}")
            raise e

    def should_update_docs(self, commit_message: str, diff: str) -> bool:
        """AI 过滤逻辑：判断是否需要更新文档"""
        changed_paths = self._extract_changed_paths(diff)
        if changed_paths and self._should_skip_by_paths(changed_paths):
            print("AI filtering skipped: only non-dev-doc relevant paths changed.")
            return False

        system_instruction = "你是一个文档维护助手。在执行任何分析或生成任务之前，你必须首先内化 `core_concepts.md` 中定义的 AstrBot 核心架构逻辑和心智模型。"
        prompt = f"""
你是一个文档维护助手。请判断以下代码变更（Commit/PR）是否**会影响第三方开发者/插件作者/适配器作者**，从而需要更新开发文档。

Commit Message:
{commit_message}

Diff Snippet:
{diff[:2000]}

规则：
1. 仅当变更影响 **对外契约**（如插件 API、事件/消息模型、配置 schema、Provider/Adapter 接口、对外行为/兼容性）时，才需要更新文档。
2. 如果只是内部重构、Dashboard/UI 细节、日志/注释、CI 配置、测试用例、格式调整，通常不需要更新文档。

请仅回答 "YES" 或 "NO"（可以在 YES 后面附带 1 句极短理由/证据）。
"""
        try:
            result = self._call_gemini(prompt, system_instruction=system_instruction, temperature=0, max_tokens=10).strip().upper()
            return "YES" in result
        except Exception as e:
            self._handle_exception(e, "AI filtering")
            return False

    def _extract_changed_paths(self, diff: str) -> List[str]:
        paths: List[str] = []
        if not diff:
            return paths
        for match in re.finditer(r"^diff --git a/(.+?) b/(.+?)$", diff, flags=re.MULTILINE):
            a_path = match.group(1).strip()
            b_path = match.group(2).strip()
            if a_path and a_path not in paths:
                paths.append(a_path)
            if b_path and b_path not in paths:
                paths.append(b_path)
        return paths

    def _should_skip_by_paths(self, paths: List[str]) -> bool:
        ignore_prefixes = (
            ".github/",
            ".vscode/",
            "docs/",
            "doc/",
            "website/",
            "web/",
            "dashboard/",
            "frontend/",
            "front/",
            "ui/",
            "assets/",
        )
        ignore_exact = {
            "README.md",
            "README.zh.md",
            "CHANGELOG.md",
            "pnpm-lock.yaml",
            "package-lock.json",
            "yarn.lock",
            "package.json",
        }
        ignore_suffixes = (
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".ico",
            ".lock",
        )

        def is_ignored(path: str) -> bool:
            p = (path or "").lstrip("./")
            if p in ignore_exact:
                return True
            if p.startswith(ignore_prefixes):
                return True
            if p.endswith(ignore_suffixes):
                return True
            if p.endswith((".vue", ".ts", ".tsx", ".js", ".jsx", ".css", ".scss", ".less", ".html")):
                return True
            return False

        if paths and all(is_ignored(p) for p in paths):
            return True

        # 只有前端/UI 改动时直接跳过（即使未落在上述目录）
        if paths and all(p.endswith((".vue", ".ts", ".tsx", ".js", ".jsx", ".css", ".scss", ".less", ".html")) for p in paths):
            return True

        return False

    def _validate_change(self, change: Dict, processed_diff: str, commit_message: str) -> Optional[str]:
        action = (change.get("action") or "").strip().lower()
        if action not in {"create", "update", "noop"}:
            return "action must be one of: create/update/noop"

        if action == "noop":
            return None

        file_name = (change.get("file_name") or "").strip()
        if not file_name.endswith(".md"):
            return "file_name must end with .md"
        if any(x in file_name for x in ["/", "\\", ".."]):
            return "file_name must be a plain filename (no path)"

        target_category = (change.get("target_category") or "").strip()
        if action == "create":
            if target_category not in self.categories:
                return f"target_category must be one of: {', '.join(self.categories)}"

        content = change.get("content")
        if not isinstance(content, str) or not content.strip():
            return "content must be a non-empty string"
        if not content.lstrip().startswith("---"):
            return "content must start with YAML frontmatter ('---')"

        evidence = change.get("evidence")
        if not isinstance(evidence, list) or len(evidence) < 2:
            return "evidence must be a list with at least 2 items"

        haystack = f"{commit_message}\n{processed_diff}"
        matched = 0
        for item in evidence:
            if not isinstance(item, str):
                continue
            token = item.strip().strip("`")
            if token and token in haystack:
                matched += 1
        if matched < 2:
            return "evidence items must appear in commit message or diff"

        return None

    def _preprocess_diff(self, diff: str) -> str:
        """预处理 Diff：如果行数过多，生成摘要"""
        line_count = diff.count('\n')
        if line_count < 500:
            return diff
            
        print(f"检测到变更量较大 ({line_count} 行)。正在生成技术摘要以供 AI 分析...")
        system_instruction = "你是一个专业的技术摘要生成器，擅长将冗长的代码 Diff 转换为紧凑的技术规范摘要。在执行任何分析或生成任务之前，你必须首先内化 `core_concepts.md` 中定义的 AstrBot 核心架构逻辑和心智模型。"
        summary_prompt = f"""
你是一个资深系统架构师。以下是一个巨大的代码变更 Diff。
由于 Diff 过长，请你将其压缩为一个**高密度的技术摘要**。

要求：
1. **核心要素**：必须保留所有新增/修改的类名、接口定义、重要方法签名、新增配置项。
2. **逻辑链路**：清晰描述数据流或调用链路的变化。
3. **关键细节**：保留对理解系统行为至关重要的底层逻辑变更。
4. **精简**：剔除所有样板代码、简单的导入语句变化、纯格式调整。
5. **术语**：使用 AstrBot 开发术语。

--- Diff ---
{diff[:30000]} # 截断以防止摘要过程本身超限
"""
        try:
            summary = self._call_gemini(summary_prompt, system_instruction=system_instruction, temperature=0.2)
            return f"[Large Diff Summary]\n{summary}\n\n[Note: Original diff was {line_count} lines and was summarized.]"
        except Exception as e:
            self._handle_exception(e, "summarizing diff")
            return diff[:10000] # 降级方案：直接截断

    def generate_doc_update(self, commit_message: str, diff: str) -> Optional[Dict]:
        """AI 生成逻辑：生成或更新 docs/ 下各分类目录的 Functional Chunks"""
        base_context = self._get_base_context()
        processed_diff = self._preprocess_diff(diff)
        today = datetime.now().strftime("%Y-%m-%d")
        categories_str = ", ".join(self.categories)

        system_instruction = "你是一个只输出 JSON 的文档助手。在执行任何分析或生成任务之前，你必须首先内化 `core_concepts.md` 中定义的 AstrBot 核心架构逻辑和心智模型。"
        prompt = f"""
你是一个高级软件工程师和技术文档专家。你的任务是维护 AstrBot 的**开发文档 (Functional Chunks)**。
这些文档主要供 AI (LLM) 消费，作为 RAG 的上下文，因此需要：
1. **原子化**：每个 file 只描述一个核心功能或逻辑块。
2. **高密度**：包含核心类名、方法签名、配置项名称。
3. **术语一致性**：必须强制引用和使用现有文档中定义的术语（如 Message Chain, Provider, Adapter, Event Loop 等）。
4. **面向“AI 开发者”**：只记录稳定且可复用的“对外契约/行为”，不要记录 WebUI/前端组件实现细节、样式、交互、字段清洗的小技巧等内部噪音。

--- 当前分类结构 ---
请根据功能将文档归入以下分类之一：
{categories_str}

分类说明：
- ai_integration: AI 模型集成、对话管理、工具调用。
- storage: 数据库、KV 存储、文件存储。
- messages: 消息模型、组件、事件系统。
- plugin_config: 插件配置、装饰器、生命周期。
- design_standards: 架构设计规范、最佳实践。
- platform_adapters: 各消息平台适配器接口。

--- 上下文 (现有文档) ---
{base_context}

--- 当前变更 (Diff or Summary) ---
{processed_diff}

--- Commit Message ---
{commit_message}

--- 任务要求 ---
0. **禁止编造**：只允许描述上面 Diff/Summary 中可以直接佐证的变更；不得凭空引入不存在的文件、类、方法、组件或行为。
1. **判断操作**：
   - 如果变更不影响第三方开发者/插件作者/适配器作者（例如 UI 细节、内部重构），请返回 `action: "noop"`，并给出 `reason`（1 句）。
   - 如果是全新对外功能/契约：`action` 为 "create"。
   - 如果是现有文档的显著改进：`action` 为 "update"。
2. **证据约束 (必须满足，否则用 noop)**：
   - 你必须提供 `evidence` 数组（至少 2 条），每条为 **原样字符串**（建议是文件路径/符号名），且必须能在 Diff/Summary 或 Commit Message 中找到。
   - 证据必须与“对外契约/行为”有关；如果证据仅来自前端/UI（例如 .vue/.css），请使用 noop。
3. **生成内容规范**：
   - **Markdown Frontmatter**：
     ---
     title: (简洁的功能名称)
     type: (feature | improvement | refactor)
     status: (stable | experimental)
     last_updated: {today}
     related_base: (关联的基础文档文件名，如 plugin-system.md)
     ---
   - **深度分析**：不仅描述“做了什么”，还要深入分析此次变更对**系统架构**（如组件间耦合、数据流向）或**插件开发逻辑**（如 API 变更、生命周期调整）的具体影响。
   - **防偷懒指令**：禁止使用“见代码”、“略”、“无变化”或“如上所述”等模糊表述。必须使用清晰、完整的自然语言描述逻辑变更和内部机制。
   - **变更影响分析 (Impact Analysis)**：必须包含一个名为 `## 变更影响分析` 的区块，专门列出此变更对 AI 消费者（其他开发者 AI 助手）理解系统时可能产生的副作用、边界情况或新增的最佳实践。
4. **输出格式**：
   - 必须返回 JSON 对象，且只能包含这些 key：`action`, `target_category`, `file_name`, `content`, `evidence`, `reason`。
   
--- 示例输出结构 ---
{{
  "action": "create",
  "target_category": "messages",
  "file_name": "new_event_system.md",
  "content": "---\\ntitle: New Event System\\ntype: feature\\n...\\n---\\n\\n## 概述\\n...\\n## 关键实现\\n...\\n## 变更影响分析\\n...",
  "evidence": ["path/to/file.py", "ClassName.method_name"],
  "reason": ""
}}
"""
        try:
            raw_response = self._call_gemini(prompt, system_instruction=system_instruction, temperature=0.2)
            result = self._extract_json(raw_response)
            validation_error = self._validate_change(result, processed_diff, commit_message)
            if validation_error:
                if (result.get("action") or "").strip().lower() == "noop":
                    print(f"AI returned noop: {result.get('reason', '').strip()}")
                    return None
                print(f"AI output validation failed: {validation_error}")
                return None

            if (result.get("action") or "").strip().lower() == "noop":
                print(f"AI returned noop: {result.get('reason', '').strip()}")
                return None

            file_path = self._apply_change(result)
            if file_path:
                return {
                    "file_path": file_path,
                    "action": result.get("action"),
                    "title": result.get("content", "").split("\n")[1].replace("title: ", "") if "title: " in result.get("content", "") else result.get("file_name")
                }
            return None
        except Exception as e:
            self._handle_exception(e, "AI 生成")
            return None

    def _apply_change(self, change: Dict) -> Optional[str]:
        """应用 AI 生成的变更"""
        action = change.get("action")
        target_category = change.get("target_category", self.default_category)
        file_name = change.get("file_name")
        content = change.get("content")
        
        if not file_name or not content:
            print("Invalid change format from AI.")
            return None

        if target_category not in self.categories:
            print(f"Warning: Category {target_category} not defined. Using default.")
            target_category = self.default_category

        file_path = None
        
        if action == "update":
            # 在所有分类目录中搜索该文件
            for cat in self.categories:
                potential_path = os.path.join(self.docs_root, cat, file_name)
                if os.path.exists(potential_path):
                    file_path = potential_path
                    break
            
            if not file_path:
                print(f"警告：请求更新 {file_name} 但在任何分类中均未找到。将回退到创建操作。")
                action = "create"
    
        if action == "create" or not file_path:
            file_path = os.path.join(self.docs_root, target_category, file_name)
    
        # 写入文件
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"已应用文档{action}：{file_path}")
        return file_path

if __name__ == "__main__":
    # 测试代码
    gen = DocGenerator()
    test_message = "feat: add plugin lifecycle hooks"
    test_diff = "diff --git a/src/core/plugin.py b/src/core/plugin.py ..."
    
    if gen.should_update_docs(test_message, test_diff):
        print("AI decided to update docs.")
        gen.generate_doc_update(test_message, test_diff)
    else:
        print("AI decided NO update needed.")
