# -*- coding: utf-8 -*-
"""
本地雷达数据引擎 (radar_sync.py)
功能：抓取/生成热点数据 -> 保存为 JSON -> 自动 Push 到 GitHub -> 触发 Netlify 部署
"""
import json
import os
import time
import datetime
import subprocess

# 你的 Netlify 绑定的本地仓库路径（如果脚本就在仓库目录下，写 '.' 即可）
REPO_PATH = "."
JSON_FILENAME = "radar_latest.json"

def get_hot_topics():
    """
    这里是你的抓取逻辑。为了让你立刻跑通测试，这里先返回高质量的 Mock 数据。
    后续你可以把这里替换为读取 TrendRadar 数据库，或者调用真实爬虫的代码。
    """
    return {
        "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topics": [
            {
                "platform": "知乎",
                "title": "职场内耗的3个底层来源是什么？",
                "hotness": "980w 热度",
                "summary": "AI总结：深入探讨了现代职场中情绪劳动、边界感缺失和向上管理失败带来的精神消耗，并提出了创客思维的破局点。",
                "url": "https://www.zhihu.com"
            },
            {
                "platform": "36Kr",
                "title": "DeepSeek API 彻底改变了独立开发者的变现逻辑",
                "hotness": "全站第一",
                "summary": "AI总结：分析了低成本大模型如何让单人团队也能构建复杂的 SaaS 应用，商业模式从'卖软件'转向'卖工作流'。",
                "url": "https://36kr.com"
            },
            {
                "platform": "微信公众号",
                "title": "为什么现在的年轻人都在搞'数字极简'？",
                "hotness": "10w+ 阅读",
                "summary": "AI总结：信息过载导致的注意力涣散，促使年轻人重新使用 MP3 和纸质书，这背后是对个人精力管理的重新夺回。",
                "url": "https://mp.weixin.qq.com"
            }
        ]
    }

def save_to_json(data):
    file_path = os.path.join(REPO_PATH, JSON_FILENAME)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ 数据已保存至 {JSON_FILENAME}")

def git_push_to_netlify():
    """自动执行 Git 命令，推送到远程仓库触发 Netlify"""
    try:
        print("正在推送到 GitHub 触发 Netlify 更新...")
        # 进入仓库目录
        os.chdir(REPO_PATH)
        
        # Git 自动化三步曲
        subprocess.run(["git", "add", JSON_FILENAME], check=True, capture_output=True)
        commit_msg = f"Auto update radar data: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        # 如果没有改动，commit 会报错，所以我们忽略 commit 的报错
        subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True)
        subprocess.run(["git", "push"], check=True, capture_output=True)
        
        print("🎉 推送成功！Netlify 将在几十秒内完成全球 CDN 刷新。")
    except subprocess.CalledProcessError as e:
        print(f"❌ 推送失败，请检查 Git 配置或网络: {e.stderr.decode('utf-8', errors='ignore')}")

def main():
    print("🚀 雷达自动化引擎已启动...")
    while True:
        # 1. 获取最新数据
        data = get_hot_topics()
        # 2. 写入本地文件
        save_to_json(data)
        # 3. 推送到云端
        git_push_to_netlify()
        
        # 每隔 2 小时（7200秒）更新一次
        print("等待下一次更新 (2小时后)...\n")
        time.sleep(7200)

if __name__ == "__main__":
    main()