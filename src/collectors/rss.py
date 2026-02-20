import feedparser
from typing import List
from datetime import datetime
from ..core.models import Article
from ..core.utils import setup_logging

logger = setup_logging(__name__)

class RSSCollector:
    def __init__(self, feed_urls: List[str]):
        self.feed_urls = feed_urls

    def fetch_articles(self, max_per_feed: int = 10) -> List[Article]:
        all_articles = []
        for url in self.feed_urls:
            try:
                logger.info(f"Fetching feed: {url}")
                feed = feedparser.parse(url)
                for entry in feed.entries[:max_per_feed]:
                    article = self._parse_entry(entry, url)
                    all_articles.append(article)
                logger.info(f"Fetched {len(feed.entries[:max_per_feed])} articles from {url}")
            except Exception as e:
                logger.error(f"Error fetching feed {url}: {e}")
        return all_articles

    def _parse_entry(self, entry, source_url: str) -> Article:
        published_date = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published_date = datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            published_date = datetime(*entry.updated_parsed[:6])

        description = entry.get('summary', entry.get('description', ''))
        content = description
        if hasattr(entry, 'content') and entry.content:
            content = entry.content[0].get('value', description)
        elif hasattr(entry, 'summary_detail'):
            content = entry.summary_detail.get('value', description)

        return Article(
            title=entry.get('title', 'Untitled'),
            description=description,
            content=content,
            url=entry.get('link', ''),
            published_date=published_date,
            source_url=source_url
        )
