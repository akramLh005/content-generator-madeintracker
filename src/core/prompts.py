from .models import Article

# ---------------------------------------------------------------------------
# Brand Voice & Identity
# ---------------------------------------------------------------------------

BRAND_VOICE = """
BRAND IDENTITY — EasyUDI
EasyUDI is the go-to platform for medical device companies navigating MDR/IVDR
compliance. We combine expert human guidance with smart, automated tools to
simplify UDI generation, EUDAMED registration, and label printing.

TARGET AUDIENCE:
Medical device manufacturers, authorized representatives, importers, and
quality/regulatory professionals across the EU.

TONE GUIDELINES:
- Conversational yet authoritative — like a senior consultant explaining over coffee.
- Use active voice, first-person plural ("we", "our"), and address the reader
  directly ("you", "your").
- Alternate short, punchy sentences with longer explanatory ones for rhythm.
- Use rhetorical questions and friendly transitions to maintain engagement.
- Avoid jargon unless necessary; when used, define it immediately in plain terms.

FORMATTING RULES:
- Short paragraphs (2-4 sentences max).
- Frequent subheadings (H2/H3) to create scannable structure.
- Bullet points for lists of 3+ items.
- Bold key terms and takeaways.
"""

# ---------------------------------------------------------------------------
# System Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a senior medical device regulatory content strategist with deep "
    "expertise in EU MDR/IVDR, EUDAMED, UDI systems, and FDA regulations. "
    "You write in French for a professional European audience. Your content is "
    "factually precise, strategically structured for SEO, and reflects the "
    "EasyUDI brand voice: accessible, expert, and reassuring."
)

IMAGE_SYSTEM_PROMPT = """You are an expert visual prompt engineer specializing in professional infographic design for the medical device regulatory industry. Your sole job is to craft a single, detailed image-generation prompt (for DALL-E 3 / Stable Diffusion / FLUX) that will produce a high-quality infographic illustration.

STRICT OUTPUT RULES:
- Output ONLY the final image-generation prompt. No explanations, no preamble, no commentary.
- The prompt you generate must explicitly forbid any text, words, letters, numbers, or captions in the image.

VISUAL STYLE REQUIREMENTS:
1. Style: Clean flat-vector / isometric infographic illustration, sharp lines, professional finish.
2. Composition: Square format (1:1), single centered focal point with supporting elements arranged symmetrically around it.
3. Color palette: Deep navy (#1B2A4A), professional blue (#4A90D9), white (#FFFFFF), warm gold accent (#F5C518). Subtle gradients allowed.
4. Visual metaphors: Use industry-relevant icons and symbols — shields (compliance), gears (process), medical crosses, documents, checkmarks, connected nodes, circuit motifs.
5. Mood: Trustworthy, modern, authoritative — suitable for a professional blog header.
6. Absolutely NO text, words, labels, watermarks, or lettering of any kind inside the image.
"""

# ---------------------------------------------------------------------------
# Content Generation Prompts
# ---------------------------------------------------------------------------

def get_blog_prompt(article: Article) -> str:
    source_content = article.content or article.description
    return f"""{BRAND_VOICE}

TASK:
Transform the source article below into an original, SEO-optimized blog post
for the EasyUDI blog. Do NOT simply rephrase — add expert analysis, practical
implications, and actionable takeaways for our audience.

SOURCE ARTICLE:
- Title: {article.title}
- Content: {source_content}
- Original URL: {article.url}

STRUCTURE (follow precisely):
1. **Headline** — SEO-friendly, 55-70 characters, in an <h1> tag.
2. **Hook paragraph** — Open with a bold statement, a surprising stat, or a
   direct question that makes the reader want to continue.
3. **3-4 body sections** — Each with a clear <h2> subheading. Cover:
   - What happened / what changed
   - Why it matters for medical device companies
   - Practical impact and what to do next
4. **Conclusion with CTA** — Summarize the key takeaway and invite the reader
   to explore EasyUDI's compliance tools.

CONTENT RULES:
- Length: 800-1200 words.
- Language: French.
- Seamlessly integrate keywords: MDR, IVDR, EUDAMED, UDI, dispositif médical,
  conformité réglementaire — but NEVER keyword-stuff.
- Include one internal-link placeholder: [LIEN_EASYUDI] where a link to
  EasyUDI's relevant feature page should go.
- Format as clean HTML (<h1>, <h2>, <p>, <ul>, <strong>). No <html>/<body> wrappers.
- Cite the source article naturally within the text.

OUTPUT: Return ONLY the HTML content. No code fences, no markdown.
"""


def get_linkedin_prompt(title: str, summary: str, url: str) -> str:
    return f"""{BRAND_VOICE}

TASK:
Write an engaging LinkedIn post to promote a new blog article published on the
EasyUDI blog. Optimize for reach and engagement on the LinkedIn platform.

BLOG ARTICLE TO PROMOTE:
- Title: {title}
- Summary: {summary}
- URL: {url}

POST STRUCTURE (follow this formula):
1. **Hook** (line 1-2): A bold opening statement, provocative question, or
   surprising insight. This line determines whether people click "see more" —
   make it impossible to scroll past.
2. **Context** (3-5 lines): Briefly explain the news or topic. What happened?
   Why should the reader care?
3. **Key Insight** (2-3 lines): Share one practical takeaway or expert opinion.
4. **CTA** (1-2 lines): Drive action — invite to read the full article, comment,
   or share their experience.
5. **Hashtags**: Include 5-7 relevant hashtags on the last line.

FORMAT RULES:
- Language: French.
- Length: 150-250 words.
- Use line breaks between sections for readability (LinkedIn rewards whitespace).
- Use 2-3 emojis MAX — strategically placed, not decorative.
- Mandatory hashtags: #MDR #IVDR #EUDAMED #MedicalDevices #EasyUDI
  (add 2-3 topic-specific ones).
- Professional yet approachable tone.

OUTPUT: Return ONLY the post text. No surrounding quotes, no markdown.
"""


def get_email_prompt(title: str, summary: str, url: str) -> str:
    return f"""{BRAND_VOICE}

TASK:
Create a conversion-focused email campaign to announce a new blog article to
EasyUDI's subscriber list.

BLOG ARTICLE INFO:
- Title: {title}
- Summary: {summary}
- URL: {url}

EMAIL STRUCTURE:
1. **Subject line** — 35-50 characters, curiosity-driven or benefit-focused.
   Avoid spammy words (free, urgent, act now).
2. **Preview text** — 80-100 characters that complement (not repeat) the subject.
3. **Email body** (HTML):
   - Personal greeting: "Bonjour,"
   - Opening: 1-2 sentences connecting to a pain point or current event.
   - Core value: 2-3 short paragraphs explaining what the article covers and
     why it matters to the reader.
   - Primary CTA button text: Clear, action-oriented (e.g., "Lire l'article complet").
   - Sign-off: Warm closing from "L'équipe EasyUDI".

FORMAT RULES:
- Language: French.
- Body as clean HTML.
- Keep total email body under 200 words — concise and scannable.

OUTPUT: Return a valid JSON object with exactly these keys:
{{"subject": "...", "preview": "...", "body_html": "..."}}

Return ONLY the JSON. No code fences, no commentary.
"""


# ---------------------------------------------------------------------------
# Image Prompt Generation
# ---------------------------------------------------------------------------

def get_image_prompt(title: str, summary: str) -> str:
    """Build a contextual user-message for the IMAGE_SYSTEM_PROMPT.

    Extracts the article's core theme and feeds it to the LLM so the
    generated image prompt is unique and relevant to the specific article,
    not a generic medical-device illustration.
    """
    return f"""ARTICLE CONTEXT:
- Title: {title}
- Summary: {summary}

INSTRUCTIONS:
Based on the article context above, generate ONE detailed image-generation
prompt for a professional infographic illustration that visually captures the
core theme of this specific article.

Your prompt must:
1. Identify the article's main concept (e.g., new regulation deadline, EUDAMED
   update, UDI compliance change) and translate it into a visual metaphor.
2. Describe specific objects, icons, and compositional layout relevant to THIS
   article — not generic medical imagery.
3. Specify the flat-vector / isometric infographic style, the navy-blue-gold
   color palette, and the square 1:1 format.
4. Explicitly state: "No text, words, letters, numbers, or captions in the image."

OUTPUT: Return ONLY the image-generation prompt. Nothing else.
"""
