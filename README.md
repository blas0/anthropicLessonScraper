# Anthropic Lesson Scraper

A Python tool that extracts the **educational "Lesson" sections** from [Anthropic's prompt engineering interactive tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) notebooks.

## 🎯 What This Does

Instead of manually going through each Jupyter notebook to find the lesson content, this scraper:

- **Fetches** all tutorial notebooks directly from GitHub's raw JSON API
- **Extracts** only the "Lesson" sections (the core educational content)
- **Filters out** setup code, exercises, and examples 
- **Outputs** clean markdown files ready for study or reference

## 🚀 Quick Start

```bash
# Clone this repository
git clone https://github.com/yourusername/anthropic-lesson-scraper.git
cd anthropic-lesson-scraper

# Install dependencies
pip install -r requirements.txt

# Test the scraper
python test_scraper.py

# Run the full scraper
python anthropic_lesson_scraper.py
```

## 📋 What Gets Scraped

The tool extracts lesson content from these 9 confirmed notebook files:

- **01_Basic_Prompt_Structure** - API fundamentals and required parameters
- **02_Being_Clear_and_Direct** - Writing effective prompts  
- **03_Assigning_Roles_Role_Prompting** - Using system prompts and roles
- **04_Separating_Data_and_Instructions** - XML tags and data formatting
- **05_Formatting_Output_and_Speaking_for_Claude** - Output control techniques
- **06_Precognition_Thinking_Step_by_Step** - Chain of thought prompting
- **07_Using_Examples_Few-Shot_Prompting** - Learning from examples
- **08_Avoiding_Hallucinations** - Accuracy and reliability techniques  
- **09_Complex_Prompts_from_Scratch** - Advanced prompt construction

## 🎛️ Output Options

When you run the scraper, choose your preferred format:

**Option 1: Individual Files**
```
lesson_01_Basic_Prompt_Structure.md
lesson_02_Being_Clear_and_Direct.md
lesson_03_Assigning_Roles_Role_Prompting.md
...
```

**Option 2: Combined File**
```
all_lessons.md  (all lessons in one file)
```

## 🔧 How It Works

**Smart Content Extraction:**
- Parses Jupyter notebook JSON structure directly
- Identifies `## Lesson` markdown headers automatically  
- Stops before `### Examples` or `## Exercises` sections
- Skips code cells and focuses on educational content

**Example extracted content:**
```markdown
## Lesson

Anthropic offers two APIs, the legacy Text Completions API and the current Messages API. 
For this tutorial, we will be exclusively using the Messages API.

At minimum, a call to Claude using the Messages API requires the following parameters:
* `model`: the API model name of the model that you intend to call
* `max_tokens`: the maximum number of tokens to generate before stopping
* `messages`: an array of input messages...
```

**Why This Approach:**
- ✅ **Robust**: Uses GitHub's raw API instead of fragile HTML scraping
- ✅ **Targeted**: Gets only lesson content, not setup or examples
- ✅ **Maintainable**: Clean code with proper error handling
- ✅ **Respectful**: Includes rate limiting for GitHub's servers

## 📚 Programmatic Usage

Use it as a Python library for custom processing:

```python
from anthropic_lesson_scraper import AnthropicLessonScraper

scraper = AnthropicLessonScraper()

# Get a single lesson
notebook = scraper.fetch_notebook("01_Basic_Prompt_Structure.ipynb")
content = scraper.extract_lesson_content(notebook)

# Get all lessons
lessons = scraper.scrape_all_lessons()

# Process as needed
for filename, lesson_data in lessons.items():
    title = lesson_data['title'] 
    content = lesson_data['content']
    # Your custom processing here...
```

## 🛠️ Files Included

- **`anthropic_lesson_scraper.py`** - Main scraper class and CLI
- **`test_scraper.py`** - Validation test (run this first!)
- **`example_usage.py`** - Shows programmatic usage patterns
- **`requirements.txt`** - Just `requests>=2.28.0`

## 🔍 Example Output

Here's what the extracted lesson content looks like:

```markdown
# Chapter 1: Basic Prompt Structure

*Source: 01_Basic_Prompt_Structure.ipynb*

## Lesson

Anthropic offers two APIs, the legacy Text Completions API and the current Messages API. 
For this tutorial, we will be exclusively using the Messages API.

At minimum, a call to Claude using the Messages API requires the following parameters:

* `model`: the API model name of the model that you intend to call
* `max_tokens`: the maximum number of tokens to generate before stopping. 
  Note that Claude may stop before reaching this maximum...
```

## 🤝 Contributing

This tool focuses specifically on lesson extraction. If you'd like to extend it:

- **Add other content sections** (exercises, examples) 
- **Support different output formats** (JSON, HTML, etc.)
- **Add filtering options** (by topic, difficulty, etc.)
- **Improve content parsing** for edge cases

## 📄 License

MIT License - feel free to use, modify, and distribute.

## 🙏 Credits

- Educational content source: [Anthropic's Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- This tool simply extracts and reformats their excellent educational material

---

**Note**: This scraper is an independent tool and is not officially associated with Anthropic. It's designed to make their public educational content more accessible for study and reference.
