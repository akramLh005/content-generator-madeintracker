import json
import os
from typing import List
from .models import Article
from .utils import setup_logging

logger = setup_logging(__name__)

class RelevanceFilter:
    def __init__(self, keywords_file: str = "keywords.json"):
        self.primary: List[str] = []
        self.secondary: List[str] = []
        self.negative: List[str] = []
        self._load_keywords(keywords_file)

    def _load_keywords(self, path: str):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.primary = [k.lower() for k in data.get('primary_keywords', [])]
                self.secondary = [k.lower() for k in data.get('secondary_keywords', [])]
                self.negative = [k.lower() for k in data.get('negative_keywords', [])]
        else:
            logger.warning(f"Keywords file not found: {path}")

    def score_articles(self, articles: List[Article], min_score: float = 0.5) -> List[Article]:
        scored = []
        for article in articles:
            score = self._calculate_score(article)
            if score >= min_score:
                article.relevance_score = score
                scored.append(article)
        
        scored.sort(key=lambda x: x.relevance_score, reverse=True)
        logger.info(f"Filtered {len(scored)} relevant articles from {len(articles)} total")
        return scored

    def _calculate_score(self, article: Article) -> float:
        text = f"{article.title} {article.description} {article.content}".lower()
        
        for neg in self.negative:
            if neg in text:
                return 0.0
        
        p_matches = sum(1 for kw in self.primary if kw in text)
        s_matches = sum(1 for kw in self.secondary if kw in text)
        
        p_score = min(p_matches / 3, 1.0) if self.primary else 0.0
        s_score = min(s_matches / 5, 1.0) if self.secondary else 0.0
        
        total_score = (p_score * 0.6) + (s_score * 0.4)
        return round(float(total_score), 3)
