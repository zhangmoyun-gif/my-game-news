import json
import os
from datetime import datetime, timedelta

# 导入我们自定义的抓取模块
from crawler import fetch_articles_from_all_sources, remove_duplicate_articles
from processor import filter_and_rank_articles

def main():
    print("开始获取游戏行业资讯...")
    print("=" * 50)

    # 1. 从所有数据源获取文章（启用去重）
    all_articles = fetch_articles_from_all_sources()
    all_articles = remove_duplicate_articles(all_articles)
    print(f"去重后共获取到 {len(all_articles)} 篇文章")

    # 2. 使用规则库进行筛选和排名
    ranked_articles = filter_and_rank_articles(all_articles)
    print(f"关键词筛选后剩下 {len(ranked_articles)} 篇重要文章")

    # 3. 准备新游数据 (示例数据，后续会替换为真实抓取)
    new_games = [
        {
            "name": "《宿命回响：弦上的叹息》",
            "platform": ["手游"],
            "genre": ["RPG", "音乐"],
            "release_date": "2023-10-18",
            "estimated_downloads": "150万",
            "estimated_revenue": "500万"
        },
        {
            "name": "《战锤40K：暗潮》",
            "platform": ["PC", "Xbox"],
            "genre": ["FPS", "合作"],
            "release_date": "2023-10-17",
            "estimated_downloads": "50万",
            "estimated_revenue": "300万"
        },
        {
            "name": "《铃兰之剑：为这和平的世界》",
            "platform": ["手游"],
            "genre": ["SRPG", "策略"],
            "release_date": "2023-10-20",
            "estimated_downloads": "80万",
            "estimated_revenue": "200万"
        }
    ]

    # 4. 生成最终的数据结构
    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "top_articles": ranked_articles[:15],  # 保留前15篇最重要的
        "new_games": new_games
    }

    # 5. 将数据写入docs目录下的JSON文件，供网页读取
    docs_dir = "docs"
    os.makedirs(docs_dir, exist_ok=True)
    
    with open(os.path.join(docs_dir, "data.json"), "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("=" * 50)
    print("数据更新完成！")
    print(f"最后更新: {output_data['last_updated']}")
    print(f"重要文章: {len(ranked_articles)} 篇")
    print(f"新游数据: {len(new_games)} 款")

if __name__ == "__main__":
    main()
