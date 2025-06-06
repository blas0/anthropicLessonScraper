#!/usr/bin/env python3
"""
Example usage of the Anthropic Lesson Scraper
"""

from anthropic_lesson_scraper import AnthropicLessonScraper

def main():
    """Example of how to use the scraper programmatically"""
    
    # Initialize the scraper
    scraper = AnthropicLessonScraper()
    
    # Option 1: Scrape a single lesson
    print("Fetching a single lesson...")
    notebook = scraper.fetch_notebook("01_Basic_Prompt_Structure.ipynb")
    if notebook:
        title = scraper.get_lesson_title(notebook)
        content = scraper.extract_lesson_content(notebook)
        print(f"Title: {title}")
        print(f"Content preview: {content[:200]}...")
    
    # Option 2: Scrape all lessons and process them
    print("\nFetching all lessons...")
    lessons = scraper.scrape_all_lessons()
    
    # Process the lessons however you want
    for filename, lesson_data in lessons.items():
        print(f"\n📖 {lesson_data['title']}")
        print(f"   Source: {filename}")
        print(f"   Length: {len(lesson_data['content'])} characters")
        
        # You could do custom processing here:
        # - Extract specific patterns
        # - Store in a database
        # - Transform the content
        # - etc.
    
    # Save to custom format or location
    scraper.save_lessons(lessons, 'combined')

if __name__ == "__main__":
    main()
