#!/usr/bin/env python3
"""
Comprehensive test suite for the Anthropic Lesson Scraper

This script validates that the scraper can:
1. Fetch individual notebooks from GitHub
2. Extract lesson content correctly
3. Handle multiple lessons without errors
4. Provide meaningful error messages
"""

import sys
import os

# Add current directory to path so we can import the scraper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anthropic_lesson_scraper import AnthropicLessonScraper

def test_single_lesson():
    """Test fetching and parsing a single lesson"""
    print("🧪 Testing scraper with a single lesson...")
    
    scraper = AnthropicLessonScraper()
    
    # Test with the basic prompt structure lesson
    filename = "01_Basic_Prompt_Structure.ipynb"
    notebook = scraper.fetch_notebook(filename)
    
    if not notebook:
        print("❌ Failed to fetch notebook")
        return False
    
    title = scraper.get_lesson_title(notebook)
    content = scraper.extract_lesson_content(notebook)
    
    print(f"📖 Title: {title}")
    
    if not content:
        print("❌ No lesson content extracted")
        return False
    
    print(f"📝 Content length: {len(content)} characters")
    print(f"📝 Content preview: {content[:200]}...")
    
    # Check if the content contains expected patterns from the example
    expected_patterns = [
        "Anthropic offers two APIs",
        "Messages API",
        "model",
        "max_tokens",
        "messages"
    ]
    
    found_patterns = []
    for pattern in expected_patterns:
        if pattern.lower() in content.lower():
            found_patterns.append(pattern)
    
    print(f"✅ Found {len(found_patterns)}/{len(expected_patterns)} expected patterns: {found_patterns}")
    
    if len(found_patterns) >= 3:  # At least 3 out of 5 patterns should be found
        print("✅ Test passed! Scraper is working correctly.")
        return True
    else:
        print("❌ Test failed - content doesn't match expected patterns")
        return False

def test_multiple_lessons():
    """Test fetching multiple lessons to verify overall functionality"""
    print("\n🧪 Testing multiple lesson extraction...")
    
    scraper = AnthropicLessonScraper()
    lessons = scraper.scrape_all_lessons()
    
    print(f"📊 Successfully extracted {len(lessons)} lessons")
    
    # Verify we got a reasonable number of lessons
    if len(lessons) >= 8:  # We expect around 9 lessons
        print("✅ Got expected number of lessons")
        return True
    else:
        print(f"❌ Expected at least 8 lessons, got {len(lessons)}")
        return False

def main():
    """Run comprehensive tests"""
    print("🔬 Running Anthropic Lesson Scraper Tests\n")
    
    try:
        # Test 1: Single lesson extraction
        test1_success = test_single_lesson()
        
        # Test 2: Multiple lesson extraction (only if first test passes)
        test2_success = False
        if test1_success:
            test2_success = test_multiple_lessons()
        
        # Summary
        print("\n" + "="*50)
        print("📋 TEST SUMMARY")
        print("="*50)
        print(f"Single lesson test: {'✅ PASS' if test1_success else '❌ FAIL'}")
        print(f"Multiple lessons test: {'✅ PASS' if test2_success else '❌ FAIL'}")
        
        if test1_success and test2_success:
            print("\n🎉 All tests passed! The scraper is ready to use.")
            print("\n📋 Next steps:")
            print("   1. Run: python anthropic_lesson_scraper.py")
            print("   2. Choose your output format (individual or combined files)")
            print("   3. Find your extracted lessons in the current directory")
        else:
            print("\n❌ Some tests failed. Check your internet connection and try again.")
            print("\n🔧 Troubleshooting:")
            print("   - Ensure you have internet access")
            print("   - Check if GitHub is accessible")
            print("   - Verify requests library is installed: pip install requests")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        print("\n🔧 This might be a network issue or missing dependency.")

if __name__ == "__main__":
    main()
