#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import tempfile
from pathlib import Path
from ebooklib import epub
from bs4 import BeautifulSoup
import bs4

# CSS styles to support dark theme
DARK_THEME_CSS = """
@media (prefers-color-scheme: dark) {
    body {
        color: #f0f0f0 !important;
        background-color: #121212 !important;
    }
    
    p, h1, h2, h3, h4, h5, h6, li, span, div {
        color: #f0f0f0 !important;
    }
    
    a {
        color: #90caf9 !important;
    }
    
    b, strong {
        color: #ffffff !important;
        font-weight: bold !important;
    }
}
"""

def convert_to_bionic_str(soup, text):
    """Converts text to bionic format"""
    new_parent = soup.new_tag("span")
    
    # Break text into words and spaces/punctuation
    words = re.split(r'(\s+|\W+)', text)
    
    for word in words:
        # If it's a space or punctuation, add it as is
        if not word.strip() or not any(c.isalnum() for c in word):
            new_parent.append(soup.new_string(word))
            continue
            
        # For words 2 or more characters long
        if len(word) >= 2:
            # The first half of the word (just over half)
            mid = len(word) // 2
            if len(word) > 2:
                mid += 1
                
            first_half = word[:mid]
            second_half = word[mid:]
            
            # Create a <b> tag for the first half
            b_tag = soup.new_tag("b")
            b_tag.string = first_half
            new_parent.append(b_tag)
            
            # Add the other half
            new_parent.append(soup.new_string(second_half))
        else:
            # Short words are added as they are
            new_parent.append(soup.new_string(word))
    
    return new_parent

def process_html_content(content, add_dark_theme=True):
    """Processes HTML content"""
    soup = BeautifulSoup(content, 'html.parser')
    
    # Add dark theme support
    if add_dark_theme:
        # Check if the <head> tag is present
        head = soup.head
        if not head:
            head = soup.new_tag("head")
            if soup.html:
                soup.html.insert(0, head)
            else:
                html = soup.new_tag("html")
                html.append(head)
                soup.append(html)
                
        # Add CSS styles for the dark theme
        style_tag = soup.new_tag("style")
        style_tag.string = DARK_THEME_CSS
        head.append(style_tag)
    
    # Process text elements
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        for child in list(tag.children):
            if isinstance(child, bs4.element.NavigableString) and child.strip():
                child.replace_with(convert_to_bionic_str(soup, child.text))
    
    return str(soup)

def convert_epub_to_bionic(input_path, output_path=None, add_dark_theme=True):
    """Converts EPUB file to bionic format"""
    # Determine the output path
    if output_path is None:
        base_name = os.path.basename(input_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(os.path.dirname(input_path), f"Bionic_{name}{ext}")
    
    try:
        print(f"EPUB file download: {input_path}")
        source = epub.read_epub(input_path)
        
        # If you want to add the CSS file for the dark theme as a separate resource
        if add_dark_theme:
            # Create a CSS file
            css_item = epub.EpubItem(
                uid="style_dark_theme",
                file_name="styles/dark_theme.css",
                media_type="text/css",
                content=DARK_THEME_CSS.encode('utf-8')
            )
            source.add_item(css_item)
            
            # Add the CSS file to the style list
            if not hasattr(source, 'spine') or not source.spine:
                source.spine = []
        
        # Process each HTML element
        print("Processing the contents of a book...")
        items_processed = 0
        
        for item in source.get_items():
            if item.media_type == "application/xhtml+xml":
                items_processed += 1
                print(f"Document processing: {item.get_name()}")
                
                content = item.content.decode('utf-8')
                # Process the content by adding a dark theme
                item.content = process_html_content(content, add_dark_theme).encode('utf-8')
                
                # Add a link to the CSS file, if one has been created
                if add_dark_theme:
                    soup = BeautifulSoup(item.content, 'html.parser')
                    head = soup.head
                    if head:
                        # Check if there is already a link to our CSS file
                        link_exists = False
                        for link in head.find_all('link', {'href': 'styles/dark_theme.css'}):
                            link_exists = True
                            break
                            
                        if not link_exists:
                            link_tag = soup.new_tag("link", href="styles/dark_theme.css", rel="stylesheet", type="text/css")
                            head.append(link_tag)
                            item.content = str(soup).encode('utf-8')
        
        # Save the result
        print(f"Saves the converted file: {output_path}")
        epub.write_epub(output_path, source)
        
        print(f"Conversion completed. Documents processed: {items_processed}")
        return output_path
    
    except Exception as e:
        print(f"Error during file processing: {e}")
        import traceback
        print(traceback.format_exc())
        raise

def main():
    """Basic function to run from the command line"""
    if len(sys.argv) < 2:
        print("Usage: python bionic_converter.py <path_to_epub_file> [save_path]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result_path = convert_epub_to_bionic(input_path, output_path, add_dark_theme=True)
        print(f"The file has been successfully converted and saved: {result_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()