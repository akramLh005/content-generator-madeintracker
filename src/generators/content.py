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
        self.model = settings.groq_model

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
            # Reasoning models like gpt-oss-120b often prefer max_completion_tokens 
            # and might not support response_format="json_object" simultaneously with reasoning.
            # We'll adapt based on the model name.
            kwargs = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": cfg["temperature"],
            }

            if "gpt-oss" in self.model.lower():
                kwargs["max_completion_tokens"] = cfg["max_tokens"]
                kwargs["reasoning_effort"] = "medium"
                # If we use reasoning, some models might fail if response_format is also set 
                # or if the prompt doesn't strictly follow JSON rules.
                # However, the user request used it via console. 
                # Groq documentation says for JSON mode, the word "json" MUST be in the prompt.
            else:
                kwargs["max_tokens"] = cfg["max_tokens"]
            
            if cfg.get("response_format") == "json_object":
                # Ensure "json" is in the prompt if we use response_format
                if "json" not in prompt.lower() and "json" not in SYSTEM_PROMPT.lower():
                    prompt += "\nReturn output in valid JSON format."
                
                # Reasoning models like gpt-oss often fail Groq's strict JSON validation 
                # even when outputting valid JSON. We bypass strict mode for them.
                if "gpt-oss" not in self.model.lower():
                    kwargs["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
