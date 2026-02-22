import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import random
from ..core.config import settings
from ..core.models import Article, GeneratedContent
from ..core.prompts import get_image_prompt
from ..core.utils import setup_logging
from ..collectors.rss import RSSCollector
from ..collectors.scraper import WebScraper
from ..generators.content import ContentGenerator
from ..generators.image import ImageGenerator

logger = setup_logging(__name__)

class ContentPipeline:
    def __init__(self):
        self.rss_collector = RSSCollector(settings.rss_feeds_list)
        self.web_scraper = WebScraper(settings.competitor_urls)
        self.content_gen = ContentGenerator()
        self.image_gen = ImageGenerator()
        self.output_dir = Path(settings.output_dir)

    def run(self) -> Optional[Path]:
        logger.info("Starting MadeInTracker Content Pipeline")
        
        articles = self.rss_collector.fetch_articles()
        scraped_articles = self.web_scraper.scrape_all()
        articles.extend(scraped_articles)
        
        if not articles:
            logger.error("No articles collected from any source.")
            return None

        # Deduplicate all collected articles by title
        unique_articles = []
        seen_titles = set()
        for art in articles:
            normalized_title = art.title.strip().lower()
            if normalized_title not in seen_titles:
                unique_articles.append(art)
                seen_titles.add(normalized_title)
        
        logger.info(f"Unique articles collected ({len(unique_articles)}): {[a.title[:50] + '...' for a in unique_articles]}")
        
        # Select a random article from the full pool
        top = random.choice(unique_articles)
        logger.info(f"Randomly selected: {top.title}")
        
        blog_html = self.content_gen.generate_blog(top)
        linkedin = self.content_gen.generate_linkedin(top.title, top.description, str(top.url))
        email = self.content_gen.generate_email(top.title, top.description, str(top.url))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = self.output_dir / timestamp
        folder.mkdir(parents=True, exist_ok=True)
        
        image_path = None
        # Generate a dynamic visual prompt based on the article context
        vision_prompt = self.content_gen.generate_image_prompt(top.title, top.description)
        logger.info(f"Generated Vision Prompt: {vision_prompt}")
        
        raw_image = self.image_gen.generate(vision_prompt, str(folder / "original.png"))
        if raw_image:
            image_path = self.image_gen.add_overlay(
                raw_image, 
                ' '.join(top.title.split()[:4]), 
                str(folder / "formatted.png")
            )

        generated = GeneratedContent(
            article_title=top.title,
            blog_html=blog_html,
            linkedin_post=linkedin,
            email_campaign=email,
            image_path=os.path.basename(image_path) if image_path else None,
            source_article=top
        )
        
        self._save_outputs(folder, generated)
        self._create_preview(folder, generated)
        
        logger.info(f"Success! Content saved to {folder}")
        return folder

    def _save_outputs(self, folder: Path, content: GeneratedContent):
        (folder / "blog.html").write_text(content.blog_html, encoding='utf-8')
        (folder / "linkedin.txt").write_text(content.linkedin_post, encoding='utf-8')
        (folder / "email.json").write_text(content.email_campaign.model_dump_json(indent=2), encoding='utf-8')
        (folder / "metadata.json").write_text(content.model_dump_json(indent=2), encoding='utf-8')

    def _create_preview(self, folder: Path, content: GeneratedContent):
        img_html = f'<img src="{content.image_path}" class="brand-image">' if content.image_path else ""
        
        preview_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MadeInTracker Content: {content.article_title}</title>
    <style>
        :root {{
            --brand-yellow: #F8D568;
            --brand-green: #217346;
            --brand-blue: #3C73A8;
            --bg-gray: #f8fafc;
            --text-dark: #1e293b;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', -apple-system, sans-serif; 
            background: var(--bg-gray); 
            color: var(--text-dark); 
            line-height: 1.6; 
            padding: 40px 20px;
        }}
        
        .container {{ 
            max-width: 1100px; 
            margin: 0 auto; 
        }}
        
        .header {{ 
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            border-left: 8px solid var(--brand-green);
        }}
        
        .header h1 {{ font-size: 24px; color: var(--brand-green); margin-bottom: 10px; }}
        .header .meta {{ font-size: 14px; color: #64748b; }}
        .header a {{ color: var(--brand-blue); text-decoration: none; font-weight: 500; }}

        .grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }}
        
        .card {{ 
            background: white; 
            border-radius: 12px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.05); 
            padding: 30px; 
            margin-bottom: 30px;
            transition: transform 0.2s ease;
        }}
        
        .card:hover {{ transform: scale(1.005); }}
        
        .section-tag {{ 
            display: inline-block; 
            padding: 4px 12px; 
            border-radius: 20px; 
            font-size: 12px; 
            font-weight: 700; 
            text-transform: uppercase; 
            margin-bottom: 15px;
        }}
        
        .tag-linkedin {{ background: #e0f2fe; color: var(--brand-blue); }}
        .tag-email {{ background: #dcfce7; color: var(--brand-green); }}
        .tag-blog {{ background: #fef9c3; color: #854d0e; }}
        
        h2 {{ font-size: 20px; margin-bottom: 15px; color: #334155; }}
        
        .brand-image {{ 
            width: 100%; 
            border-radius: 8px; 
            margin-bottom: 25px; 
            border: 1px solid #e2e8f0; 
        }}
        
        pre {{ 
            white-space: pre-wrap; 
            font-family: inherit; 
            background: #f1f5f9; 
            padding: 20px; 
            border-radius: 8px; 
            font-size: 14px;
        }}
        
        .email-meta {{ 
            background: #fff;
            border: 1px dashed var(--brand-yellow); 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 20px; 
        }}
        
        .blog-content h1, .blog-content h2 {{ color: var(--brand-blue); margin: 20px 0 10px; }}
        .blog-content p {{ margin-bottom: 15px; }}
        
        @media (max-width: 850px) {{
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>MadeInTracker AI Engine</h1>
            <div class="meta">
                Source : <a href="{content.source_article.url}" target="_blank">{content.article_title}</a> | 
                Generated at {content.generated_at.strftime("%Y-%m-%d %H:%M")}
            </div>
        </header>
        
        <div class="grid">
            <div class="main-column">
                <div class="card">
                    <span class="section-tag tag-blog">Article de Blog</span>
                    {img_html}
                    <div class="blog-content">
                        {content.blog_html}
                    </div>
                </div>
            </div>
            
            <div class="side-column">
                <div class="card">
                    <span class="section-tag tag-linkedin">Post LinkedIn</span>
                    <pre>{content.linkedin_post}</pre>
                </div>
                
                <div class="card">
                    <span class="section-tag tag-email">Campagne Emailing</span>
                    <div class="email-meta">
                        <strong>Objet :</strong> {content.email_campaign.subject}<br>
                        <strong>Aperçu :</strong> {content.email_campaign.preview}
                    </div>
                    <div class="email-body">
                        {content.email_campaign.body_html}
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
        (folder / "preview.html").write_text(preview_html, encoding='utf-8')
