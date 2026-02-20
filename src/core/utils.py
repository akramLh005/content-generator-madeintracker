import json
import logging
import os
import re
from typing import Dict, Optional
from PIL import ImageFont

def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(name)

logger = setup_logging(__name__)

def clean_json_string(json_str: str) -> str:
    json_str = re.sub(r'```json\s*', '', json_str)
    json_str = re.sub(r'```\s*', '', json_str)
    return json_str.strip()

def get_font(size: int = 48) -> ImageFont.FreeTypeFont:
    paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

def extract_json_fallback(text: str) -> Optional[dict]:
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(clean_json_string(match.group(0)))
    except Exception as e:
        logger.warning(f"Fallback JSON extraction failed: {e}")
    return None
