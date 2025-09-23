# 这是我们确认的关键词规则库
KEYWORDS = {
    "high_priority": {
        "companies": ["腾讯", "网易", "米哈游", "字节跳动", "莉莉丝", "叠纸", "鹰角"],
        "events": ["版号", "财报", "裁员", "招聘", "融资", "收购", "流水", "下载量", "破纪录"]
    },
    "medium_priority": {
        "trends": ["AI", "AIGC", "UE5", "云游戏", "海外市场"]
    }
}

def filter_and_rank_articles(articles):
    """根据关键词规则库对文章进行筛选和排名"""
    ranked_articles = []
    
    for article in articles:
        score = 0
        tags = []
        text = article["title"] + " " + article.get("summary", "")
        
        # 检查高优先级关键词
        for category, words in KEYWORDS["high_priority"].items():
            for word in words:
                if word in text:
                    score += 3  # 高优先级词得3分
                    tags.append(word)
        
        # 检查中优先级关键词
        for category, words in KEYWORDS["medium_priority"].items():
            for word in words:
                if word in text:
                    score += 1  # 中优先级词得1分
                    if word not in tags:  # 避免重复
                        tags.append(word)
        
        # 如果文章有得分，则保留
        if score > 0:
            article["score"] = score
            article["tags"] = list(set(tags))  # 去重
            ranked_articles.append(article)
    
    # 按得分从高到低排序
    ranked_articles.sort(key=lambda x: x["score"], reverse=True)
    return ranked_articles
