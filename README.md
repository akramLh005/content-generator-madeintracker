
# MadeInTracker AI Content Generator - POC

![Workflow Diagram](workflow_diagram.PNG)

🎯 **Proof of Concept** - AI-powered content generator for medical device compliance articles

## Overview

This tool automatically generates brand-aligned content from medical device regulatory news:
- ✍️ **Blog Articles** 
- 📱 **LinkedIn Posts** 
- 📧 **Email Campaigns** 
- 🎨 **AI-Generated Images**

## Installation & Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Run the Generator

```bash
python main.py
```

The project will:
1. 📰 Collect articles from RSS feeds
2. 🔍 Filter for medical device compliance topics
3. ✍️ Generate blog article, LinkedIn post, and email
4. 🎨 Create AI image with French text
5. 💾 Save everything to `generated_content/TIMESTAMP/`
6. 🌐 Open preview in your browser

## Scheduling Daily Generation

You can schedule the generator to run automatically every day at a specific time using the built-in scheduler.

### Using the built-in scheduler

Run the following command to start the scheduler:

```bash
# Run daily at 09:00 (default)
python main.py --schedule

# Run daily at a custom time (e.g., 14:30)
python main.py --schedule --time 14:30
```

> [!NOTE]
> When running with `--schedule`, the tool will perform an immediate initial run, then remain active and run again every day at the specified time.

### Windows Task Scheduler (Recommended)

For a more robust setup on Windows (where the task runs even if you aren't manually keeping a terminal open), you can use the **Windows Task Scheduler**:

1. Open **Task Scheduler**.
2. Click **Create Basic Task...**.
3. Set the trigger to **Daily** and choose your time.
4. Action: **Start a program**.
5. Program/script: Path to your `python.exe` (inside the `venv`).
6. Add arguments: `main.py`.
7. Start in: The full path to your project folder.

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

### "Groq API key required"
- Make sure `.env` file exists with `GROQ_API_KEY=...`

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

## License

This is a proof-of-concept for PMSMP evaluation.

## Support

For questions or issues during the PMSMP:
- Contact: Akram Lahmar
- Company: MadeInTracker
- Email: akr.lahmar@gmail.com

