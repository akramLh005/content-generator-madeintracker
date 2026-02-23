import os
from typing import Dict, List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    groq_api_key: str
    hf_token: Optional[str] = None
    content_sources: List[Dict[str, str]] = [
        {"url": "https://medtecheurope.org/feed/", "type": "rss"},
        {"url": "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/medwatch/rss.xml", "type": "rss"},
        {"url": "https://www.medtechdive.com/", "type": "scraper"},
        {"url": "https://www.emergobyul.com/news", "type": "scraper"},
        {"url": "https://www.qualitiso.com/articles/", "type": "scraper"},
        {"url": "https://www.tracekey.com/knowledge-base/", "type": "scraper"},
        {"url": "https://www.rimsys.io/blog", "type": "scraper"},
        {"url": "https://www.innovit.com/insights", "type": "scraper"},
        {"url": "https://www.ackomas.com/", "type": "scraper"},
        {"url": "https://www.veeva.com/medtech/resources/", "type": "scraper"},
        {"url": "https://www.obelis.net/news/", "type": "scraper"},
    ]
    output_dir: str = "./generated_content"
    min_relevance_score: float = 0.3
    groq_model: str = "openai/gpt-oss-120b"
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    @property
    def hf_api_url(self) -> str:
        return f"https://router.huggingface.co/hf-inference/models/{self.hf_image_model}"

# Default LLM settings for tasks
TASK_SETTINGS = {
    "blog": {"temperature": 0.3, "max_tokens": 4000, "response_format": "text"},
    "linkedin": {"temperature": 0.3, "max_tokens": 3000, "response_format": "text"},
    "email": {"temperature": 0.3, "max_tokens": 4000, "response_format": "json_object"}
}

settings = Settings()
