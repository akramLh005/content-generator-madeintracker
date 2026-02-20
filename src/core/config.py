import os
from typing import Dict, List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    groq_api_key: str
    hf_token: Optional[str] = None
    rss_feeds: str = "https://medtecheurope.org/feed/,https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/medwatch/rss.xml"
    output_dir: str = "./generated_content"
    min_relevance_score: float = 0.3
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    @property
    def rss_feeds_list(self) -> List[str]:
        return [f.strip() for f in self.rss_feeds.split(',') if f.strip()]

    competitor_urls: List[str] = [
        "https://www.medtechdive.com/",
        "https://www.p36.io/newsroom/",
        "https://www.massdevice.com/",
        "https://www.emergobyul.com/news",
        "https://www.qualitiso.com/articles/",
        "https://www.tracekey.com/knowledge-base/",
        "https://www.rimsys.io/blog",
        "https://www.innovit.com/insights",
        "https://www.ackomas.com/",
        "https://www.veeva.com/medtech/resources/",
        "https://www.obelis.net/news/",
        "https://www.dmexperts.fr/en/medical-devices-news/",
        "https://eudamed.com/news"
    ]

# Default LLM settings for tasks
TASK_SETTINGS = {
    "blog": {"temperature": 0.7, "max_tokens": 4000, "response_format": "text"},
    "linkedin": {"temperature": 0.7, "max_tokens": 3000, "response_format": "text"},
    "email": {"temperature": 0.2, "max_tokens": 2000, "response_format": "json_object"}
}

settings = Settings()
