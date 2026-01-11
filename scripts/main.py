import os
import shutil
import sys
import time
import argparse
from typing import List, Dict
from monitor import GitHubMonitor
from doc_gen import DocGenerator
from config import config

class MainController:
    def __init__(self):
        self.monitor = GitHubMonitor()
        self.doc_gen = DocGenerator()
        self.updated_files = set()
        self.ai_changes = [] # 记录 AI 改动的详细摘要

    def handle_release(self, update: Dict):
        """
        实现版本发布逻辑：
        当检测到新 Tag 时，自动将当前 docs/ 下的所有分类文件夹（排除 snapshots/）拷贝到 docs/snapshots/<version>/ 下。
        """
        tag_name = update.get('tag_name')
        if not tag_name:
            return

        snapshot_path = os.path.join("docs/snapshots", tag_name)
        docs_path = "docs"

        print(f"🚀 检测到新版本发布：{tag_name}。正在创建文档快照...")
        
        if not os.path.exists(docs_path):
            print(f"⚠️ 警告：{docs_path} 不存在。跳过快照创建。")
            return

        # 确保目录创建安全
        os.makedirs("docs/snapshots", exist_ok=True)
        if os.path.exists(snapshot_path):
            print(f"⚠️ 警告：快照目录 {snapshot_path} 已存在。将执行覆盖。")
            shutil.rmtree(snapshot_path)

        os.makedirs(snapshot_path, exist_ok=True)

        try:
            # 遍历 docs 下的项，排除 snapshots
            for item in os.listdir(docs_path):
                if item == "snapshots":
                    continue
                
                src_item = os.path.join(docs_path, item)
                dst_item = os.path.join(snapshot_path, item)
                
                if os.path.isdir(src_item):
                    shutil.copytree(src_item, dst_item)
                else:
                    shutil.copy2(src_item, dst_item)
            
            print(f"✅ 快照已创建至 {snapshot_path}")
            
            # 记录更新的文件（递归添加快照目录下的所有文件）
            for root, _, files in os.walk(snapshot_path):
                for file in files:
                    self.updated_files.add(os.path.join(root, file))
        except Exception as e:
            print(f"❌ 创建快照时出错：{e}")

    def handle_commit(self, update: Dict, force: bool = False):
        """
        实现 PR 自动化辅助：处理 Commit，由 AI 判断并生成/更新文档。
        """
        sha = update.get('sha', 'unknown')
        message = update.get('message', '')
        diff = update.get('diff', '')

        print(f"📝 正在分析提交 {sha[:7]}...")
        
        try:
            if force or self.doc_gen.should_update_docs(message, diff):
                print(f"✨ AI 决定为提交 {sha[:7]} 更新文档。")
                result = self.doc_gen.generate_doc_update(message, diff)
                if result:
                    file_path = result['file_path']
                    self.updated_files.add(file_path)
                    self.ai_changes.append(result)
            else:
                print(f"ℹ️ AI 决定无需为提交 {sha[:7]} 更新文档。")
        except Exception as e:
            print(f"❌ 处理提交 {sha[:7]} 时出错：{e}")

    def run(self, force_latest: bool = False):
        print("=== AstrBot 文档自动化同步开始 ===")
        try:
            # 1. 获取变更
            updates, new_state = self.monitor.check_for_updates(force_latest=force_latest)
            
            if not updates:
                print("🏁 未发现新变更。退出。")
                return

            # 2. 顺序处理变更
            processed_updates = []
            for update in updates:
                if update['type'] == 'release':
                    self.handle_release(update)
                    processed_updates.append(update)
                elif update['type'] == 'commit':
                    self.handle_commit(update, force=force_latest)
                    processed_updates.append(update)

            # 3. 只有在所有文件写入成功后，才更新 state.json
            self.monitor.save_state(new_state)
            print("💾 状态记录已更新。")
            
            # 4. PR 自动化输出
            self.output_summary(processed_updates)

        except Exception as e:
            print(f"💥 主循环出现严重错误：{e}")
            sys.exit(1)
        print("=== AstrBot 文档自动化同步完成 ===")

    def output_summary(self, updates: List[Dict]):
        if not self.updated_files:
            print("📝 没有文件被创建或更新。")
            return
            
        print("\n" + "="*20 + " 总结 " + "="*20)
        print(f"总计更新文件数: {len(self.updated_files)}")
        for f in self.updated_files:
            print(f"- {f}")
        
        # GitHub Action 环境变量输出
        if os.getenv("GITHUB_ACTIONS") == "true":
            github_output = os.getenv("GITHUB_OUTPUT")
            if github_output:
                # 构造 PR 标题和描述
                latest_update = updates[-1] if updates else {}
                if latest_update.get('type') == 'release':
                    tag_name = latest_update.get('tag_name')
                    pr_title = f"docs: 自动同步版本发布 {tag_name}"
                    pr_body = f"🚀 检测到 AstrBot 新版本发布：`{tag_name}`。\n\n本 PR 自动创建了该版本的文档快照。"
                else:
                    sha = latest_update.get('sha', '')[:7]
                    pr_title = f"docs: 自动同步提交 {sha}"
                    pr_body = f"📝 基于提交 `{latest_update.get('sha', '')}` 自动更新文档。\n\n"
                    
                    if self.ai_changes:
                        pr_body += "### 🤖 AI 改动分析\n"
                        for change in self.ai_changes:
                            action_str = "创建" if change['action'] == "create" else "更新"
                            pr_body += f"- **{action_str}** `{change['file_path']}`: {change['title']}\n"
                        pr_body += "\n"
                    
                    pr_body += "**深度分析包含：**\n"
                    pr_body += "- **架构影响**：深入分析此次改动对 AstrBot 核心组件的影响。\n"
                    pr_body += "- **内部逻辑**：记录内部机制和数据流的变更。\n"
                    pr_body += "- **AI 上下文优化**：针对 RAG 和 AI 开发者优化的结构化分析。\n\n"
                    pr_body += f"**原始提交信息**: {latest_update.get('message', '').splitlines()[0]}"

                with open(github_output, "a", encoding="utf-8") as f:
                    f.write("has_updates=true\n")
                    f.write(f"files_count={len(self.updated_files)}\n")
                    f.write(f"pr_title={pr_title}\n")
                    # GHA multiline output format
                    f.write("pr_body<<EOF\n")
                    f.write(f"{pr_body}\n")
                    f.write(f"\n**更新文件列表**：\n")
                    for file in self.updated_files:
                        f.write(f"- {file}\n")
                    f.write("EOF\n")
            
            print("[GHA] has_updates=true")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AstrBot Docs Automation")
    parser.add_argument("--force-latest", action="store_true", help="Force sync with the latest commit")
    args = parser.parse_args()

    controller = MainController()
    controller.run(force_latest=args.force_latest)
