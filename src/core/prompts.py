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
    "EasyUDI brand voice: accessible, expert, and reassuring. "
    "If a JSON response is requested, you MUST return ONLY valid JSON."
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
Write a high-engagement LinkedIn post promoting a new EasyUDI blog article.
Optimize for reach, clarity, and professional impact.

ARTICLE:
Title: {title}
Summary: {summary}
URL: {url}

STRUCTURE:
1. Hook (1–2 lines): Strong opening statement or question that stops scrolling.
2. Context (3–5 lines): Explain what’s new and why it matters.
3. Key insight (2–3 lines): One practical takeaway or expert perspective.
4. CTA (1–2 lines): Invite readers to read, comment, or share.
5. Hashtags: 5–7 total, placed on the final line.

RULES (STRICT):
- Language: French
- Length: 150–250 words
- Use short paragraphs with line breaks (LinkedIn style)
- Use MAX 3 emojis, only if relevant
- Mandatory hashtags: #MDR #IVDR #EUDAMED #MedicalDevices #EasyUDI (+2–3 specific)
- Tone: Professional, clear, confident
- ABSOLUTELY NO markdown formatting
- NEVER use **bold**, asterisks, or styled text — LinkedIn does NOT support it
- Output must be plain text only

OUTPUT:
Return ONLY the final post text.
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
    return f"""ARTICLE CONTEXT:
Title: {title}
Summary: {summary}

TASK:
Write ONE single image-generation prompt for a professional 1:1 infographic illustration that visually communicates the specific theme of this article.

NON-NEGOTIABLE CONSTRAINTS (MUST FOLLOW):
1) ABSOLUTELY NO TEXT IN THE IMAGE.
   - The image must contain ZERO: words, letters, numbers, labels, captions, UI text, watermarks, logos with lettering, icons containing characters, signs, documents with visible writing, QR codes, barcodes, serial numbers, or “placeholder” text.
   - Do NOT include: “text overlays”, “labels”, “headlines”, “callouts”, “annotations”, “form fields”, “screens with writing”, or “poster/sign” elements.
   - If any object normally includes text (forms, screens, certificates, packaging, labels), render it as blank shapes with no glyphs.

2) SELF-CHECK BEFORE FINALIZING:
   - Re-read your prompt and remove any instruction that could lead to text appearing in the image.
   - If you accidentally wrote any text-related instruction, replace it with a clear, correctly spelled sentence stating:
     "No text, words, letters, numbers, or captions anywhere in the image."

STYLE & BRAND:
- Style: flat-vector or isometric infographic (clean, modern, professional).
- Palette: navy blue + gold accents + white background (high contrast, minimal).
- Composition: clear hierarchy, balanced spacing, 1–3 focal elements plus supporting icons.

CONTENT REQUIREMENTS:
- Identify the article’s main concept (e.g., deadline, EUDAMED update, UDI rule change, compliance workflow).
- Translate it into a concrete visual metaphor specific to THIS article (not generic medical imagery).
- Specify exact objects/icons/layout that match the article (e.g., database node for EUDAMED, supply chain/packaging for UDI, checklist/workflow for compliance, timeline for deadlines).

OUTPUT RULES (STRICT):
- Return ONE prompt only.
- Plain text only.
- No bullet lists, no numbering, no extra commentary.
"""