from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class Article(BaseModel):
    title: str
    description: str = ""
    content: str = ""
    url: HttpUrl
    published_date: Optional[datetime] = None
    source_url: HttpUrl
    relevance_score: float = 0.0

class EmailCampaign(BaseModel):
    subject: str
    preview: str
    body_html: str

class GeneratedContent(BaseModel):
    article_title: str
    blog_html: str
    linkedin_post: str
    email_campaign: EmailCampaign
    image_path: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.now)
    source_article: Article
