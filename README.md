<<<<<<< HEAD
# ai-generator
=======
# MadeInTracker AI Content Generator - POC

🎯 **Proof of Concept** - AI-powered content generator for medical device compliance articles

## Overview

This tool automatically generates brand-aligned content from medical device regulatory news:
- ✍️ **Blog Articles** (800-1200 words, SEO-optimized, in French)
- 📱 **LinkedIn Posts** (engaging, with hashtags)
- 📧 **Email Campaigns** (subject, preview, HTML body)
- 🎨 **AI-Generated Images** (with French text overlay, brand colors)

## Features

✅ Free tier APIs (Groq + Pollinations.ai)  
✅ RSS feed monitoring with relevance filtering  
✅ EasyUDI brand voice and visual guidelines  
✅ Beautiful HTML preview of all generated content  
✅ Auto-saves all outputs (HTML, TXT, JSON, PNG)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Get a **free Groq API key**:
1. Visit https://console.groq.com
2. Sign up (free)
3. Generate API key

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=your_actual_groq_api_key_here
RSS_FEEDS=https://medtecheurope.org/feed/,https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/medical-devices/rss.xml
```

### 3. Run the Generator

```bash
python main.py
```

The script will:
1. 📰 Collect articles from RSS feeds
2. 🔍 Filter for medical device compliance topics
3. ✍️ Generate blog article, LinkedIn post, and email
4. 🎨 Create AI image with French text
5. 💾 Save everything to `generated_content/TIMESTAMP/`
6. 🌐 Open preview in your browser

## Output Structure

```
generated_content/
└── 20260214_192200/
    ├── preview.html              # Beautiful visual preview (opens automatically)
    ├── blog_article.html         # Full blog post
    ├── linkedin_post.txt         # LinkedIn content
    ├── email_campaign.json       # Email data (subject, preview, body)
    ├── email_preview.html        # Email preview
    ├── article_image.png         # AI generated image
    ├── article_image_final.png   # Image with French text overlay
    └── metadata.json             # Generation metadata
```

## Configuration

### RSS Feeds

Edit `RSS_FEEDS` in `.env` to add more sources. Current defaults:
- MedTech Europe blog
- FDA Medical Devices RSS

### Keywords

Edit `keywords.json` to customize relevance filtering:
- `primary_keywords`: MDR, IVDR, EUDAMED, FDA, UDI, etc.
- `secondary_keywords`: notified body, certification, etc.
- `negative_keywords`: job posting, careers, etc.

### Brand Guidelines

Visual and tone guidelines are built-in:
- **Colors**: Yellow (#F8D568), Green (#217346), Blue (#3C73A8)
- **Style**: Flat illustration, minimal shading, medical device theme
- **Tone**: Conversational, reassuring, energetic, accessible

## Testing Individual Modules

Each module can be tested independently:

```bash
# Test RSS collector
python src/collectors/rss_collector.py

# Test content filter
python src/collectors/content_filter.py

# Test content generator (requires GROQ_API_KEY)
python src/generators/content_generator.py

# Test image generator
python src/image_gen/image_generator.py
```

## Technology Stack

| Component | Technology | License |
|-----------|------------|---------|
| LLM | Groq API (Llama 3.3 70B) | Free tier |
| Image Generation | Hugging Face (SDXL) | Free tier / Token |
| RSS Parsing | feedparser | Open source |
| HTML Parsing | BeautifulSoup4 | Open source |

## Troubleshooting

### "HF_TOKEN missing"
- Make sure `.env` file exists with `HF_TOKEN=...`
- Use the token provided in the project discussion.

### "Groq API key required"
- Make sure `.env` file exists with `GROQ_API_KEY=...`
- Get free key at https://console.groq.com

### "No articles collected"
- Check RSS feed URLs are valid
- Test feeds manually in a browser
- Check internet connection

### "No relevant articles found"
- Lower `MIN_RELEVANCE_SCORE` in `.env` (default: 0.5)
- Edit `keywords.json` to add more keywords

### Image generation fails
- Stable Diffusion XL on HF Inference API may sometimes be overloaded.
- Wait a minute and retry.
- Check that your `HF_TOKEN` is valid.

## Next Steps (Full Implementation)

After POC validation, these features can be added:
- ✨ Web scraping for competitor blogs
- ⏰ Daily automation scheduler
- 🚀 Publishing integrations (WordPress, LinkedIn API, email platforms)
- 📊 Analytics and A/B testing
- 🌐 Multi-language support
- 🔄 Content versioning and editing workflow

## Project Structure

```
pmsmp - madeintracker/
├── main.py                      # Main pipeline
├── requirements.txt             # Dependencies
├── .env.example                 # Config template
├── keywords.json                # Keyword filtering
├── src/
│   ├── collectors/
│   │   ├── rss_collector.py     # RSS feed parser
│   │   └── content_filter.py    # Relevance filtering
│   ├── generators/
│   │   ├── content_generator.py # AI content generation
│   │   └── prompt_templates.py  # LLM prompts
│   └── image_gen/
│       └── image_generator.py   # AI image generation
└── generated_content/           # Output directory
```

## License

This is a proof-of-concept for PMSMP evaluation.

## Support

For questions or issues during the PMSMP:
- Contact: Akram Lahmar
- Company: MadeInTracker
- Email: akr.lahmar@gmail.com

---

**Made with ❤️ for EasyUDI by MadeInTracker**
>>>>>>> 1df6fea (chore: initialize repository and project structure)
