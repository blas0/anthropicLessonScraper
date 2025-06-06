#!/usr/bin/env python3
"""
Anthropic Prompt Engineering Tutorial Lesson Scraper

This tool extracts the educational "Lesson" sections from Anthropic's prompt 
engineering interactive tutorial notebooks on GitHub. It provides clean, 
studyable content without the setup code, exercises, or examples.

Repository: https://github.com/anthropics/prompt-eng-interactive-tutorial
Version: 1.0
"""

import requests
import json
import re
from typing import List, Dict, Optional
from urllib.parse import quote
import time


class AnthropicLessonScraper:
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/anthropics/prompt-eng-interactive-tutorial/master/Anthropic%201P"
        self.session = requests.Session()
        # Add headers to avoid rate limiting
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_notebook_files(self) -> List[str]:
        """Get list of notebook files from the repository"""
        # These are the confirmed notebook files that exist in the repository
        files = [
            "00_Tutorial_How-To.ipynb",
            "01_Basic_Prompt_Structure.ipynb", 
            "02_Being_Clear_and_Direct.ipynb",
            "03_Assigning_Roles_Role_Prompting.ipynb",
            "04_Separating_Data_and_Instructions.ipynb",
            "05_Formatting_Output_and_Speaking_for_Claude.ipynb",
            "06_Precognition_Thinking_Step_by_Step.ipynb",
            "07_Using_Examples_Few-Shot_Prompting.ipynb",
            "08_Avoiding_Hallucinations.ipynb",
            "09_Complex_Prompts_from_Scratch.ipynb"
            # Note: Appendix files (10.x) are not consistently available in the repo
        ]
        return files
    
    def fetch_notebook(self, filename: str) -> Optional[Dict]:
        """Fetch and parse a notebook file"""
        url = f"{self.base_url}/{quote(filename)}"
        
        try:
            print(f"Fetching {filename}...")
            response = self.session.get(url)
            response.raise_for_status()
            
            notebook = json.loads(response.text)
            return notebook
            
        except requests.RequestException as e:
            print(f"❌ Error fetching {filename}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON for {filename}: {e}")
            return None
    
    def extract_lesson_content(self, notebook: Dict) -> Optional[str]:
        """Extract the lesson section content from a notebook"""
        if 'cells' not in notebook:
            return None
        
        cells = notebook['cells']
        lesson_content = []
        in_lesson_section = False
        
        for cell in cells:
            if cell.get('cell_type') != 'markdown':
                continue
                
            source = cell.get('source', [])
            if not source:
                continue
                
            # Join source lines into a single string
            content = ''.join(source)
            
            # Check if this cell starts a lesson section
            if re.search(r'^##\s+Lesson\s*$', content, re.MULTILINE | re.IGNORECASE):
                in_lesson_section = True
                # Add the lesson content (everything after the ## Lesson header)
                lesson_lines = content.split('\n')
                for i, line in enumerate(lesson_lines):
                    if re.match(r'^##\s+Lesson\s*$', line, re.IGNORECASE):
                        # Add everything after this line
                        lesson_content.extend(lesson_lines[i+1:])
                        break
                continue
            
            # Check if we've hit another major section (stop collecting)
            if in_lesson_section and re.search(r'^##\s+', content, re.MULTILINE):
                # This is another major section, stop here
                break
            
            # Check for subsections within lesson (like ### Examples)
            if in_lesson_section and re.search(r'^###\s+Examples?\s*$', content, re.MULTILINE | re.IGNORECASE):
                # Stop before examples section
                break
                
            # If we're in the lesson section, collect this cell's content
            if in_lesson_section:
                lesson_content.append(content)
        
        if lesson_content:
            # Clean up the content
            result = '\n'.join(lesson_content)
            # Remove extra whitespace and clean up
            result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)  # Multiple newlines to double
            result = result.strip()
            return result
        
        return None
    
    def get_lesson_title(self, notebook: Dict) -> str:
        """Extract the lesson title from the notebook"""
        if 'cells' not in notebook:
            return "Unknown"
        
        # Look for the main title in the first few cells
        for cell in notebook['cells'][:3]:
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                # Look for main chapter title
                match = re.search(r'^#\s+(.+)$', source, re.MULTILINE)
                if match:
                    return match.group(1).strip()
        
        return "Unknown"
    
    def scrape_all_lessons(self) -> Dict[str, Dict[str, str]]:
        """Scrape lessons from all notebook files"""
        files = self.get_notebook_files()
        lessons = {}
        
        for filename in files:
            # Add small delay to be respectful
            time.sleep(0.5)
            
            notebook = self.fetch_notebook(filename)
            if not notebook:
                continue
            
            title = self.get_lesson_title(notebook)
            lesson_content = self.extract_lesson_content(notebook)
            
            if lesson_content:
                lessons[filename] = {
                    'title': title,
                    'content': lesson_content
                }
                print(f"✅ Extracted lesson from {filename}")
            else:
                print(f"⚠️  No lesson content found in {filename}")
        
        return lessons
    
    def save_lessons(self, lessons: Dict[str, Dict[str, str]], output_format: str = 'individual'):
        """Save lessons to files"""
        if output_format == 'individual':
            # Save each lesson to a separate file
            for filename, lesson_data in lessons.items():
                # Create a clean filename
                clean_name = re.sub(r'\.ipynb$', '', filename)
                output_file = f"lesson_{clean_name}.md"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {lesson_data['title']}\n\n")
                    f.write(f"*Source: {filename}*\n\n")
                    f.write("## Lesson\n\n")
                    f.write(lesson_data['content'])
                
                print(f"💾 Saved {output_file}")
        
        elif output_format == 'combined':
            # Save all lessons to a single file
            with open('all_lessons.md', 'w', encoding='utf-8') as f:
                f.write("# Anthropic Prompt Engineering Tutorial - All Lessons\n\n")
                
                for filename, lesson_data in lessons.items():
                    f.write(f"## {lesson_data['title']}\n\n")
                    f.write(f"*Source: {filename}*\n\n")
                    f.write(lesson_data['content'])
                    f.write("\n\n---\n\n")
            
            print("💾 Saved all_lessons.md")


def main():
    """Main function to run the scraper"""
    print("🚀 Anthropic Lesson Scraper v1.0")
    print("Extracting lesson content from Anthropic's prompt engineering tutorial...\n")
    
    scraper = AnthropicLessonScraper()
    
    # Scrape all lessons
    lessons = scraper.scrape_all_lessons()
    
    if not lessons:
        print("❌ No lessons found!")
        print("\n🔧 This might be due to:")
        print("   - Network connectivity issues")
        print("   - GitHub repository changes")
        print("   - Missing requests library (run: pip install requests)")
        return
    
    print(f"\n📊 Successfully extracted {len(lessons)} lessons!")
    
    # Show what was extracted
    print("\n📝 Extracted lessons:")
    for i, (filename, lesson_data) in enumerate(lessons.items(), 1):
        print(f"   {i}. {lesson_data['title']}")
    
    # Ask user for output format
    print("\n📁 Choose output format:")
    print("1. Individual files (one .md file per lesson)")
    print("2. Combined file (all lessons in one file)")
    
    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == '1':
            scraper.save_lessons(lessons, 'individual')
            break
        elif choice == '2':
            scraper.save_lessons(lessons, 'combined')
            break
        else:
            print("⚠️  Please enter 1 or 2")
    
    print("\n✅ Scraping complete! Your lesson files are ready to study.")
    print("📖 Happy learning!")


if __name__ == "__main__":
    main()
