import arxiv
from datetime import datetime, timedelta
import config
import random

class ArxivCrawler:
    def __init__(self, keywords=None, days_back=None):
        self.keywords = keywords
        self.days_back = days_back

    def crawl(self):
        articles = []
        current_time = datetime.now().replace(tzinfo=None)
        for keyword in self.keywords:
            search = arxiv.Search(
                query=keyword,
                max_results=100,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )

            for result in search.results():
                published_date = result.published
                if current_time - published_date.replace(tzinfo=None) <= timedelta(days=self.days_back):
                    articles.append(self._format_article(result))
                else:
                    break

        print(f"总共找到 {len(articles)} 篇相关文章")
        return articles

    def get_article_by_id(self, article_id):
        try:
            search = arxiv.Search(id_list=[article_id])
            result = next(search.results())
            return self._format_article(result)
        except Exception as e:
            raise Exception(f"无法找到ID为 {article_id} 的文章: {str(e)}")

    def get_article_by_title(self, title):
        search = arxiv.Search(
            query=f'ti:"{title}"',
            max_results=1
        )
        try:
            result = next(search.results())
            return self._format_article(result)
        except StopIteration:
            raise Exception(f"无法找到标题包含 '{title}' 的文章")

    def get_random_article_by_topic(self, topic, max_results=50):
        search = arxiv.Search(
            query=topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        articles = list(search.results())
        if not articles:
            raise Exception(f"没有找到与主题 '{topic}' 相关的文章")
        
        selected = random.choice(articles)
        return self._format_article(selected)

    def _format_article(self, result):
        return {
            'title': result.title,
            'content': result.summary,
            'source': result.entry_id,
            'published_date': result.published.strftime('%Y-%m-%d'),
            'authors': [author.name for author in result.authors],
            'categories': result.categories,
            'doi': result.doi,
            'comment': result.comment,
            'journal_ref': result.journal_ref,
            'pdf_url': result.pdf_url
        }

def get_news():
    crawler = ArxivCrawler(config.KEYWORDS, config.DAYS_BACK)
    return crawler.crawl()

def get_single_article(identifier=None, title=None, topic=None):
    crawler = ArxivCrawler()
    
    if identifier:
        return crawler.get_article_by_id(identifier)
    elif title:
        return crawler.get_article_by_title(title)
    elif topic:
        return crawler.get_random_article_by_topic(topic)
    else:
        raise ValueError("必须提供文章ID、标题或主题之一")
