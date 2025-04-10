import os
import regex
import zipfile
import argparse
from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm
from typing import Optional, Dict, Any

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

class BionicConverter:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {
            'min_word_length': 3,
            'bold_ratio': 0.4,  # Ratio of word to make bold
            'skip_words': {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'},
            'skip_tags': {'script', 'style', 'pre', 'code', 'math'},
            'supported_formats': {'.html', '.xhtml', '.htm', '.txt', '.md'}
        }

    def bionic_word(self, word: str) -> str:
        """Convert a word to bionic reading format."""
        word = word.strip()
        if len(word) <= 1 or word.lower() in self.config['skip_words']:
            return word
        
        if len(word) <= self.config['min_word_length']:
            return f"<b>{word[:1]}</b>{word[1:]}"
        
        bold_length = max(1, int(len(word) * self.config['bold_ratio']))
        return f"<b>{word[:bold_length]}</b>{word[bold_length:]}"

    def process_text(self, text: str) -> str:
        """Process text content to bionic reading format."""
        if not text or not text.strip():
            return text
            
        word_pattern = regex.compile(r'\b[\p{L}\p{M}]+\b', regex.UNICODE)
        
        def replace_word(match):
            word = match.group(0)
            return self.bionic_word(word)
        
        return word_pattern.sub(replace_word, text)

    def process_html_content(self, content: str) -> str:
        """Process HTML content to bionic reading format."""
        try:
            soup = BeautifulSoup(content, 'lxml')
            
            for element in soup.find_all(text=True):
                if element.parent.name not in self.config['skip_tags']:
                    new_text = self.process_text(str(element.string))
                    new_element = BeautifulSoup(new_text, 'html.parser')
                    element.replace_with(new_element)
            
            return str(soup)
        except Exception as e:
            print(f"Warning: Error processing HTML content: {str(e)}")
            return content

    def process_file(self, input_path: str, output_path: str) -> bool:
        """Process a single file to bionic reading format."""
        try:
            _, ext = os.path.splitext(input_path)
            if ext.lower() not in self.config['supported_formats']:
                print(f"Warning: Unsupported file format: {ext}")
                return False

            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if ext.lower() in {'.html', '.xhtml', '.htm'}:
                processed_content = self.process_html_content(content)
            else:
                processed_content = self.process_text(content)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            return True
        except Exception as e:
            print(f"Error processing file {input_path}: {str(e)}")
            return False

    def process_epub(self, input_path: str, output_path: str) -> bool:
        """Process an EPUB file to bionic reading format."""
        try:
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                file_list = zip_ref.infolist()
                total_files = len(file_list)
                print(f"Total files in EPUB: {total_files}")
                
                with zipfile.ZipFile(output_path, 'w') as zip_out:
                    with tqdm(total=total_files, desc="Processing files", unit="file") as pbar:
                        for file_info in file_list:
                            try:
                                with zip_ref.open(file_info) as file:
                                    content = file.read()
                                    
                                    if file_info.filename.endswith(tuple(self.config['supported_formats'])):
                                        content = self.process_html_content(content.decode('utf-8')).encode('utf-8')
                                    
                                    zip_out.writestr(file_info, content)
                            except Exception as e:
                                print(f"Warning: Error processing file {file_info.filename}: {str(e)}")
                            
                            pbar.update(1)
                            pbar.set_postfix(current_file=file_info.filename)
            
            return True
        except Exception as e:
            print(f"Error processing EPUB: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Convert files to Bionic Reading format')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('--min-word-length', type=int, default=3, help='Minimum word length to process')
    parser.add_argument('--bold-ratio', type=float, default=0.4, help='Ratio of word to make bold')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    if os.path.exists(args.output):
        print(f"Warning: Output file '{args.output}' already exists. It will be overwritten.")

    config = {
        'min_word_length': args.min_word_length,
        'bold_ratio': args.bold_ratio
    }
    
    converter = BionicConverter(config)
    
    try:
        if args.input.lower().endswith('.epub'):
            success = converter.process_epub(args.input, args.output)
        else:
            success = converter.process_file(args.input, args.output)
            
        if success:
            print(f"Conversion complete. Output saved to '{args.output}'")
        else:
            print("Conversion failed.")
    except Exception as e:
        print(f"Error occurred during processing: {str(e)}")

if __name__ == "__main__":
    main()