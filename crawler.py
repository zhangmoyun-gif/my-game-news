import feedparser
import requests
from datetime import datetime, timedelta
import time
import random

# 为每个公众号配置信息（部分为示例RSS，后续需替换为真实源）
SOURCES_CONFIG = [
    {
        "name": "GameLook",
        "url": "https://rsshub.app/wechat/gamelook",  # 示例RSS源
        "type": "rss"
    },
    {
        "name": "游戏陀螺",
        "url": "https://rsshub.app/wechat/gamelook",  # 待替换
        "type": "rss"
    },
    # 其他公众号配置...
]

def fetch_articles_from_all_sources():
    """从所有配置的数据源获取文章"""
    all_articles = []
    
    for source in SOURCES_CONFIG:
        print(f"正在抓取 {source['name']}...")
        try:
            if source["type"] == "rss":
                articles = fetch_from_rss(source["url"], source["name"])
                all_articles.extend(articles)
            # 可以添加其他类型的抓取方式，如网页爬虫
        except Exception as e:
            print(f"抓取 {source['name']} 时出错: {e}")
        
        # 礼貌性延迟，避免请求过快
        time.sleep(random.uniform(1, 3))
    
    return all_articles

def fetch_from_rss(rss_url, source_name):
    """从RSS源抓取文章"""
    articles = []
    feed = feedparser.parse(rss_url)
    
    for entry in feed.entries:
        # 只获取最近7天的文章
        published_time = datetime(*entry.published_parsed[:6])
        if datetime.now() - published_time > timedelta(days=7):
            continue
            
        article = {
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary if hasattr(entry, 'summary') else "",
            "published": published_time.strftime("%Y-%m-%d"),
            "source": source_name
        }
        articles.append(article)
    
    return articles

# 示例：手动添加一些测试数据，用于演示
def get_sample_articles():
    """返回示例文章数据，用于演示页面效果"""
    return [
        {
            "title": "网易Q3游戏业务营收123亿元，《逆水寒》手游表现强劲",
            "link": "https://example.com/1",
            "summary": "网易最新财报显示，游戏业务保持稳定增长...",
            "published": "2023-10-26",
            "source": "GameLook"
        },
        {
            "title": "10月第二批版号下发：共87款游戏过审",
            "link": "https://example.com/2",
            "summary": "国家新闻出版署发布了10月份第二批游戏版号...",
            "source": "游戏陀螺",
            "published": "2023-10-25"
        }
    ]
