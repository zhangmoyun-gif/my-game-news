import requests
from datetime import datetime, timedelta
import time
import random
import re
import json

# 多源抓取配置
SOURCES_CONFIG = [
    {
        "name": "GameLook",
        "strategies": ["aggregator", "wechat_search"],
        "search_keywords": ["GameLook", "游戏大观"],
        "priority": 3
    },
    {
        "name": "游戏葡萄", 
        "strategies": ["aggregator", "wechat_search"],
        "search_keywords": ["游戏葡萄"],
        "priority": 3
    },
    {
        "name": "游戏陀螺",
        "strategies": ["aggregator", "wechat_search"], 
        "search_keywords": ["游戏陀螺"],
        "priority": 3
    },
    {
        "name": "游戏茶馆",
        "strategies": ["aggregator", "wechat_search"],
        "search_keywords": ["游戏茶馆"],
        "priority": 3
    },
    {
        "name": "游戏那些事",
        "strategies": ["aggregator", "wechat_search"],
        "search_keywords": ["游戏那些事"],
        "priority": 3
    },
    {
        "name": "TapTap",
        "strategies": ["aggregator", "wechat_search"],
        "search_keywords": ["TapTap", "TapTap 推荐"],
        "priority": 2
    }
]

def fetch_articles_from_all_sources():
    """从所有配置的数据源获取文章"""
    print("开始从多源抓取公众号文章...")
    all_articles = []
    
    for source in SOURCES_CONFIG:
        print(f"\n正在抓取 {source['name']}...")
        try:
            articles = fetch_articles_by_strategies(source)
            if articles:
                print(f"  → 成功获取 {len(articles)} 篇文章")
                all_articles.extend(articles)
            else:
                print(f"  → 未获取到文章，使用示例数据")
                # 添加示例数据作为兜底
                all_articles.extend(get_sample_articles_for_source(source["name"]))
                
        except Exception as e:
            print(f"  → 抓取失败: {e}")
            # 失败时使用示例数据
            all_articles.extend(get_sample_articles_for_source(source["name"]))
        
        # 礼貌性延迟
        time.sleep(random.uniform(2, 4))
    
    print(f"\n抓取完成，共获取 {len(all_articles)} 篇文章")
    return all_articles

def fetch_articles_by_strategies(source):
    """根据配置的策略顺序尝试抓取"""
    articles = []
    
    for strategy in source["strategies"]:
        try:
            if strategy == "aggregator":
                result = fetch_from_aggregator(source)
            elif strategy == "wechat_search":
                result = fetch_from_wechat_search(source)
            else:
                continue
                
            if result:
                articles.extend(result)
                break  # 一个策略成功就停止尝试
                
        except Exception as e:
            print(f"   策略 {strategy} 失败: {e}")
            continue
    
    return articles

def fetch_from_aggregator(source):
    """从聚合平台抓取文章"""
    articles = []
    
    # 模拟从聚合平台获取数据（实际会调用API）
    # 这里使用模拟数据演示流程
    for keyword in source["search_keywords"]:
        try:
            # 模拟API调用
            time.sleep(1)
            
            # 模拟返回数据
            mock_articles = [
                {
                    "title": f"{keyword}：最新行业动态分析",
                    "link": f"https://example.com/{keyword}/1",
                    "summary": f"这是{keyword}的最新行业分析文章摘要...",
                    "published": (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
                    "source": source["name"]
                },
                {
                    "title": f"{keyword}深度报道：市场趋势解读", 
                    "link": f"https://example.com/{keyword}/2",
                    "summary": f"{keyword}对当前市场趋势的深度解读...",
                    "published": (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d"),
                    "source": source["name"]
                }
            ]
            articles.extend(mock_articles)
            
        except Exception as e:
            print(f"   聚合平台抓取失败: {e}")
            continue
    
    return articles

def fetch_from_wechat_search(source):
    """通过微信搜索抓取文章"""
    articles = []
    
    for keyword in source["search_keywords"]:
        try:
            # 模拟微信搜索流程
            time.sleep(1)
            
            # 模拟搜索结果显示
            mock_articles = [
                {
                    "title": f"微信搜索：{keyword}最新文章",
                    "link": f"https://weixin.sogou.com/{keyword}/1",
                    "summary": f"通过微信搜索获取的{keyword}最新内容...",
                    "published": (datetime.now() - timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d"),
                    "source": source["name"]
                }
            ]
            articles.extend(mock_articles)
            
        except Exception as e:
            print(f"   微信搜索失败: {e}")
            continue
    
    return articles

def get_sample_articles_for_source(source_name):
    """为每个公众号提供相关的示例数据"""
    sample_templates = {
        "GameLook": [
            {
                "title": f"{source_name}：全球游戏市场最新趋势",
                "link": f"https://example.com/{source_name}/sample1",
                "summary": f"{source_name}带来的全球游戏市场深度分析...",
                "published": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
                "source": source_name
            }
        ],
        "游戏葡萄": [
            {
                "title": f"{source_name}：国内游戏行业深度观察",
                "link": f"https://example.com/{source_name}/sample1", 
                "summary": f"{source_name}对国内游戏行业的专业分析...",
                "published": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "source": source_name
            }
        ],
        # 其他公众号的示例数据...
    }
    
    return sample_templates.get(source_name, [
        {
            "title": f"{source_name}最新行业资讯",
            "link": f"https://example.com/{source_name}/sample1",
            "summary": f"这是{source_name}的最新行业资讯...",
            "published": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "source": source_name
        }
    ])

# 智能去重功能
def remove_duplicate_articles(articles):
    """基于标题相似度去重"""
    seen_titles = set()
    unique_articles = []
    
    for article in articles:
        # 简化的标题标准化
        normalized_title = re.sub(r'[^\w\u4e00-\u9fff]', '', article["title"].lower())
        
        if normalized_title not in seen_titles:
            seen_titles.add(normalized_title)
            unique_articles.append(article)
    
    return unique_articles

if __name__ == "__main__":
    # 测试代码
    articles = fetch_articles_from_all_sources()
    print(f"测试完成，共获取 {len(articles)} 篇文章")
    for article in articles[:3]:  # 显示前3篇
        print(f"- {article['title']} ({article['source']})")
