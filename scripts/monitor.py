import json
import httpx
from typing import List, Dict, Optional
from config import config

class GitHubMonitor:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {config.GITHUB_TOKEN}" if config.GITHUB_TOKEN else "",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = f"https://api.github.com/repos/{config.REPO_NAME}"
        self.client = httpx.Client(headers=self.headers, timeout=30.0)

    def _load_state(self) -> Dict:
        try:
            with open(config.STATE_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"last_commit_sha": "", "last_tag": ""}

    def _save_state(self, state: Dict):
        with open(config.STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)

    def get_latest_commits(self, since_sha: str = "") -> List[Dict]:
        """获取自 since_sha 之后的所有 commits"""
        url = f"{self.base_url}/commits"
        params = {"per_page": 20} # 默认取最近20个
        
        response = self.client.get(url, params=params)
        response.raise_for_status()
        commits = response.json()
        
        new_commits = []
        for commit in commits:
            if commit['sha'] == since_sha:
                break
            new_commits.append(commit)
        
        return new_commits

    def get_commit_diff(self, sha: str) -> str:
        """获取特定 commit 的 diff 内容"""
        url = f"{self.base_url}/commits/{sha}"
        
        response = self.client.get(url, headers={"Accept": "application/vnd.github.v3.diff"})
        response.raise_for_status()
        return response.text

    def get_latest_tags(self) -> List[Dict]:
        url = f"{self.base_url}/tags"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()

    def get_merged_pull_requests(self) -> List[Dict]:
        """获取最近关闭且已合并的 PRs"""
        url = f"{self.base_url}/pulls"
        params = {"state": "closed", "sort": "updated", "direction": "desc"}
        response = self.client.get(url, params=params)
        response.raise_for_status()
        
        prs = response.json()
        return [pr for pr in prs if pr.get("merged_at")]

    def check_for_updates(self, force_latest: bool = False):
        state = self._load_state()
        last_sha = state.get("last_commit_sha")
        last_tag = state.get("last_tag")
        
        print(f"Checking for updates in {config.REPO_NAME}...")
        
        if force_latest:
            print("Force latest mode enabled. Ignoring last_commit_sha.")
            last_sha = "FORCE_LATEST" # Special value to trigger fetching only the latest commit

        # 1. 检查 Tags
        tags = self.get_latest_tags()
        new_tags = []
        if tags:
            current_latest_tag = tags[0]['name']
            if current_latest_tag != last_tag:
                # 优化同步逻辑：减少旧版本噪音。如果发现新 Tag，只取最新的一个，不要回溯历史生成海量快照。
                new_tags = [tags[0]]
                state["last_tag"] = current_latest_tag

        # 2. 检查 Commits
        if force_latest or not last_sha:
            # 只获取最新一个 commit (初次运行或强制同步最新)
            url = f"{self.base_url}/commits"
            params = {"per_page": 1}
            response = self.client.get(url, params=params)
            response.raise_for_status()
            commits = response.json()
        else:
            commits = self.get_latest_commits(since_sha=last_sha)
            
        if commits:
            state["last_commit_sha"] = commits[0]['sha']

        # 3. 汇总变更
        changes = []
        
        # 处理 Tag (发布事件)
        for tag in reversed(new_tags):
            changes.append({
                "type": "release",
                "title": f"New Release: {tag['name']}",
                "tag_name": tag['name'],
                "sha": tag['commit']['sha']
            })

        # 处理 Commits
        for commit in reversed(commits):
            sha = commit['sha']
            message = commit['commit']['message']
            author = commit['commit']['author']['name']
            
            # 尝试关联 PR (GitHub 默认的 merge commit 格式通常包含 PR 编号)
            pr_link = ""
            if "Merge pull request #" in message:
                import re
                pr_match = re.search(r'#(\d+)', message)
                if pr_match:
                    pr_id = pr_match.group(1)
                    pr_link = f"https://github.com/{config.REPO_NAME}/pull/{pr_id}"

            diff = self.get_commit_diff(sha)
            
            changes.append({
                "type": "commit",
                "sha": sha,
                "author": author,
                "message": message,
                "pr_link": pr_link,
                "diff": diff,
            })

        return changes, state

    def save_state(self, state: Dict):
        self._save_state(state)

if __name__ == "__main__":
    monitor = GitHubMonitor()
    updates, state = monitor.check_for_updates()
    
    if not updates:
        print("No new updates.")
    else:
        for update in updates:
            print("="*50)
            if update['type'] == 'release':
                print(f"🚀 {update['title']}")
            else:
                print(f"📝 Commit: {update['sha'][:7]} by {update['author']}")
                print(f"Message: {update['message'].splitlines()[0]}")
                if update['pr_link']:
                    print(f"PR: {update['pr_link']}")
                print("-" * 20)
                print(f"Diff Snapshot:\n{update['diff'][:500]}")
            print("="*50)
