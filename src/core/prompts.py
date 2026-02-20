from .models import Article

BRAND_VOICE = """
Tone Guidelines:
- Mix short, direct sentences with longer, explanatory ones
- Use active voice and simple vocabulary
- Use first and second-person pronouns (we, you)
- Be conversational, reassuring, and energetic
- Use rhetorical questions and friendly transitions
- Avoid jargon while maintaining technical accuracy

Brand Identity:
- EasyUDI simplifies UDI generation, EUDAMED registration, and label printing
- We combine expert human guidance with smart, automated tools
- We help medical device companies achieve stress-free compliance
- Target audience: Medical device manufacturers, authorized representatives, importers

Style:
- Break up content with subheadings and short paragraphs
- Use bullet points for clarity
- Make technical topics accessible
"""

def get_blog_prompt(article: Article) -> str:
    return f"""{BRAND_VOICE}

Task: Transform the following medical device regulatory news into an engaging, SEO-optimized blog article for the EasyUDI blog.

Source Article:
Title: {article.title}
Content: {article.content or article.description}
URL: {article.url}

Requirements:
1. Create a compelling, SEO-friendly title (60-70 characters)
2. Write 800-1200 words
3. Structure: Introduction, 3-4 sections with H2 headings, Conclusion with CTA
4. Write in French
5. Format as HTML (<h1>, <h2>, <p>, <ul>, etc.)
"""

def get_linkedin_prompt(title: str, summary: str, url: str) -> str:
    return f"""{BRAND_VOICE}

Task: Create an engaging LinkedIn post to promote this blog article.

Title: {title}
Summary: {summary}
URL: {url}

Requirements:
1. Catchy hook
2. 150-300 words, short paragraphs
3. 2-3 emojis, 5-7 hashtags (#MDR #IVDR #EUDAMED #MedicalDevices)
4. Write in French, professional yet approachable
"""

def get_email_prompt(title: str, summary: str, url: str) -> str:
    return f"""{BRAND_VOICE}

Task: Create an email campaign to introduce this new blog article.

Title: {title}
Summary: {summary}
URL: {url}

Requirements:
1. Compelling Subject Line (40-50 chars)
2. Preview Text (80-100 chars)
3. Email Body in French (HTML), personal greeting, highlights, clear CTA
4. Format as JSON: {{"subject": "...", "preview": "...", "body_html": "..."}}
"""

IMAGE_SPECIALIST_PROMPT = """You are a professional image generation prompt specialist for DALL-E 3 and Midjourney. 
Your goal is to create a high-quality, minimalistic, professional infographic illustration prompt based on the provided article context.

STRICT VISUAL STYLE RULES:
1. Professional flat vector illustration style.
2. Minimalistic composition, clean lines, no clutter.
3. NO TEXT in the image. Do not include any words, titles, or taglines in the visual output.
4. Color palette: Professional blues (#4A90D9, #1B2A4A), white, and yellow accents (#F5C518).
5. Theme: Medical device regulation, technology, and compliance.
6. Square format, centered focal point.

Output ONLY the final image generation prompt. Do not include any explanations or preamble.
The prompt should describe the scene, objects, and style in detail to capture the main idea of the article.
"""

def get_vision_prompt(title: str, summary: str) -> str:
    return f"""Article Title: {title}
Article Summary: {summary}

Generate a professional, minimalistic, flat vector illustration prompt that captures the essence of this news WITHOUT including any text in the image."""
