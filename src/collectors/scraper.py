import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from urllib.parse import urljoin
from ..core.models import Article
from ..core.utils import setup_logging

logger = setup_logging(__name__)

class WebScraper:
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def scrape_all(self) -> List[Article]:
        all_articles = []
        for url in self.urls:
            try:
                logger.info(f"Scraping competitor blog: {url}")
                articles = self._scrape_site(url)
                all_articles.extend(articles)
                logger.info(f"Found {len(articles)} articles from {url}")
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")
        return all_articles

    def _scrape_site(self, url: str) -> List[Article]:
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        links = soup.find_all('a', href=True)
        potential_articles = []
        for a in links:
            href = a['href']
            text = a.get_text().strip()
            if len(text) > 20 and any(kw in href.lower() for kw in ['/blog/', '/article/', '/news/']):
                if href.startswith('/'):
                    href = urljoin(url, href)
                potential_articles.append((text, href))
        
        items = soup.find_all(['article', 'div'], class_=lambda x: x and any(kw in x.lower() for kw in ['post', 'article', 'entry', 'blog']))
        
        for item in items[:10]:
            try:
                title_tag = item.find(['h1', 'h2', 'h3', 'a'])
                if not title_tag: continue
                
                title = title_tag.get_text().strip()
                link_tag = item.find('a', href=True) or (title_tag if title_tag.name == 'a' else None)
                if not link_tag: continue
                
                link = link_tag['href']
                if not link.startswith('http'):
                    link = urljoin(url, link)
                
                if any(a.url == link for a in articles): continue

                desc_tag = item.find(['p', 'div'], class_=lambda x: x and any(kw in x.lower() for kw in ['summary', 'excerpt', 'description', 'content'])) or item.find('p')
                description = desc_tag.get_text().strip() if desc_tag else ""
                
                if len(title) > 10 and link:
                    articles.append(Article(
                        title=title,
                        description=description,
                        content=description,
                        url=link,
                        published_date=datetime.now(),
                        source_url=url
                    ))
            except Exception:
                continue
                
        if not articles:
            for title, link in potential_articles[:5]:
                articles.append(Article(
                    title=title,
                    description="",
                    content="",
                    url=link,
                    published_date=datetime.now(),
                    source_url=url
                ))
                
        return articles
