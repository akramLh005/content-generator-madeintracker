import json
from groq import Groq
from ..core.models import Article, EmailCampaign
from ..core.config import TASK_SETTINGS, settings
from ..core.prompts import get_blog_prompt, get_linkedin_prompt, get_email_prompt, get_image_prompt, SYSTEM_PROMPT, IMAGE_SYSTEM_PROMPT
from ..core.utils import setup_logging, clean_json_string, extract_json_fallback

logger = setup_logging(__name__)

class ContentGenerator:
    def __init__(self, api_key: str = settings.groq_api_key):
        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-120b"

    def generate_blog(self, article: Article) -> str:
        prompt = get_blog_prompt(article)
        cfg = TASK_SETTINGS['blog']
        return self._call_llm(prompt, cfg)

    def generate_linkedin(self, title: str, summary: str, url: str) -> str:
        prompt = get_linkedin_prompt(title, summary, url)
        cfg = TASK_SETTINGS['linkedin']
        return self._call_llm(prompt, cfg)

    def generate_email(self, title: str, summary: str, url: str) -> EmailCampaign:
        prompt = get_email_prompt(title, summary, url)
        cfg = TASK_SETTINGS['email']
        raw_response = self._call_llm(prompt, cfg)
        
        try:
            data = json.loads(clean_json_string(raw_response))
        except json.JSONDecodeError:
            logger.warning("JSON parsing failed for email, trying fallback extraction")
            data = extract_json_fallback(raw_response)
            if not data:
                data = {
                    "subject": title[:50],
                    "preview": summary[:100],
                    "body_html": raw_response
                }
        
        return EmailCampaign(**data)

    def generate_image_prompt(self, title: str, summary: str) -> str:
        prompt = get_image_prompt(title, summary)
        return self._call_llm_vision(prompt)

    def _call_llm_vision(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": IMAGE_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"Image prompt LLM call failed: {e}")
            return "Professional flat vector illustration of medical technology, minimalistic, blue and white colors."

    def _call_llm(self, prompt: str, cfg: dict) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=cfg["temperature"],
                max_tokens=cfg["max_tokens"],
                response_format={"type": "json_object"} if cfg["response_format"] == "json_object" else None
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
