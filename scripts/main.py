import os
import shutil
import sys
import time
from typing import List, Dict
from monitor import GitHubMonitor
from doc_gen import DocGenerator
from config import config

class MainController:
    def __init__(self):
        self.monitor = GitHubMonitor()
        self.doc_gen = DocGenerator()
        self.updated_files = set()

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

        print(f"🚀 Detected new release: {tag_name}. Creating snapshot...")
        
        if not os.path.exists(docs_path):
            print(f"⚠️ Warning: {docs_path} does not exist. Skipping snapshot.")
            return

        # 确保目录创建安全
        os.makedirs("docs/snapshots", exist_ok=True)
        if os.path.exists(snapshot_path):
            print(f"⚠️ Warning: Snapshot directory {snapshot_path} already exists. Overwriting.")
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
            
            print(f"✅ Snapshot created at {snapshot_path}")
            
            # 记录更新的文件（递归添加快照目录下的所有文件）
            for root, _, files in os.walk(snapshot_path):
                for file in files:
                    self.updated_files.add(os.path.join(root, file))
        except Exception as e:
            print(f"❌ Error creating snapshot: {e}")

    def handle_commit(self, update: Dict):
        """
        实现 PR 自动化辅助：处理 Commit，由 AI 判断并生成/更新文档。
        """
        sha = update.get('sha', 'unknown')
        message = update.get('message', '')
        diff = update.get('diff', '')

        print(f"📝 Analyzing commit {sha[:7]}...")
        
        try:
            if self.doc_gen.should_update_docs(message, diff):
                print(f"✨ AI decided to update docs for commit {sha[:7]}.")
                file_path = self.doc_gen.generate_doc_update(message, diff)
                if file_path:
                    self.updated_files.add(file_path)
            else:
                print(f"ℹ️ AI decided no doc update needed for commit {sha[:7]}.")
        except Exception as e:
            print(f"❌ Error processing commit {sha[:7]}: {e}")

    def run(self):
        print("=== AstrBot Docs Automation Start ===")
        try:
            # 1. 获取变更
            updates, new_state = self.monitor.check_for_updates()
            
            if not updates:
                print("🏁 No new updates found. Exit.")
                return

            # 2. 顺序处理变更
            processed_updates = []
            for update in updates:
                if update['type'] == 'release':
                    self.handle_release(update)
                    processed_updates.append(update)
                elif update['type'] == 'commit':
                    self.handle_commit(update)
                    processed_updates.append(update)

            # 3. 只有在所有文件写入成功后，才更新 state.json
            self.monitor.save_state(new_state)
            print("💾 State updated successfully.")
            
            # 4. PR 自动化输出
            self.output_summary(processed_updates)

        except Exception as e:
            print(f"💥 Critical error in main loop: {e}")
            sys.exit(1)
        print("=== AstrBot Docs Automation Finished ===")

    def output_summary(self, updates: List[Dict]):
        if not self.updated_files:
            print("📝 No files were created or updated.")
            return
            
        print("\n" + "="*20 + " SUMMARY " + "="*20)
        print(f"Total updated files: {len(self.updated_files)}")
        for f in self.updated_files:
            print(f"- {f}")
        
        # GitHub Action 环境变量输出
        if os.getenv("GITHUB_ACTIONS") == "true":
            github_output = os.getenv("GITHUB_OUTPUT")
            if github_output:
                # 构造 PR 标题和描述
                latest_update = updates[-1] if updates else {}
                if latest_update.get('type') == 'release':
                    pr_title = f"docs: update for release {latest_update.get('tag_name')}"
                    pr_body = f"Automated documentation update for release {latest_update.get('tag_name')}."
                else:
                    pr_title = f"docs: sync with commit {latest_update.get('sha', '')[:7]}"
                    pr_body = f"Automated documentation update based on commit {latest_update.get('sha', '')}.\n\n"
                    pr_body += f"**Detailed Analysis Included:**\n"
                    pr_body += f"- **Architectural Impact**: Deep dive into how this change affects AstrBot's core components.\n"
                    pr_body += f"- **Internal Logic**: Documentation of internal mechanisms and data flows.\n"
                    pr_body += f"- **AI-Ready Context**: Structured impact analysis specifically for RAG and AI developers.\n\n"
                    pr_body += f"**Source Message**: {latest_update.get('message', '').splitlines()[0]}"

                with open(github_output, "a", encoding="utf-8") as f:
                    f.write("has_updates=true\n")
                    f.write(f"files_count={len(self.updated_files)}\n")
                    f.write(f"pr_title={pr_title}\n")
                    # GHA multiline output format
                    f.write("pr_body<<EOF\n")
                    f.write(f"{pr_body}\n")
                    f.write(f"\nUpdated files:\n")
                    for file in self.updated_files:
                        f.write(f"- {file}\n")
                    f.write("EOF\n")
            
            print("[GHA] has_updates=true")

if __name__ == "__main__":
    controller = MainController()
    controller.run()
