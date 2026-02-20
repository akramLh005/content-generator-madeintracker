import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw
from typing import Optional
from ..core.config import settings
from ..core.utils import setup_logging, get_font

logger = setup_logging(__name__)

class ImageGenerator:
    def __init__(self, hf_token: Optional[str] = settings.hf_token):
        self.hf_token = hf_token
        self.model_id = "black-forest-labs/FLUX.1-schnell"
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{self.model_id}"

    def generate(self, prompt: str, output_path: str) -> Optional[str]:
        if not self.hf_token:
            logger.warning("HF_TOKEN missing, skipping image generation.")
            return None

        try:
            logger.info(f"Requests HF Image for: {prompt[:50]}...")
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.hf_token}"},
                json={"inputs": prompt},
                timeout=60
            )
            
            if response.status_code != 200:
                logger.error(f"HF API Error: {response.status_code} - {response.text}")
                return None

            img = Image.open(BytesIO(response.content))
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path)
            return output_path
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return None

    def add_overlay(self, image_path: str, text: str, output_path: str) -> str:
        try:
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            font = get_font(48)
            
            w, h = img.size
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), text, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            else:
                tw, th = draw.textsize(text, font=font)
                
            x = (w - tw) // 2
            y = h - th - 50
            
            for ox, oy in [(-2,-2), (2,2), (-2,2), (2,-2)]:
                draw.text((x+ox, y+oy), text, font=font, fill="white")
            draw.text((x, y), text, font=font, fill="#3C73A8")
            
            img.save(output_path)
            return output_path
        except Exception as e:
            logger.error(f"Overlay failed: {e}")
            return image_path
