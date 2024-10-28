import arxiv
from datetime import datetime, timedelta
import config

class ArxivCrawler:
    def __init__(self, keywords, days_back):
        self.keywords = keywords
        self.days_back = days_back

    def crawl(self):
        articles = []
        current_time = datetime.now().replace(tzinfo=None)  # 移除时区信息
        for keyword in self.keywords:
            search = arxiv.Search(
                query=keyword,
                max_results=100,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )

            for result in search.results():
                # 获取发布日期
                published_date = result.published
                if current_time - published_date.replace(tzinfo=None) <= timedelta(days=self.days_back):
                    articles.append({
                        'title': result.title,
                        'content': result.summary,
                        'source': result.entry_id,
                        'published_date': published_date.strftime('%Y-%m-%d')
                    })
                else:
                    break

        print(f"总共找到 {len(articles)} 篇相关文章")
        return articles

def get_news():
    crawler = ArxivCrawler(config.KEYWORDS, config.DAYS_BACK)
    return crawler.crawl()
