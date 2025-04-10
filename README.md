# Bionic EPUB Converter

A tool for converting EPUB files to the "bionic reading" format. Bionic format highlights the first half of each word in bold, which helps to improve reading speed and text comprehension.

## Features

- Converts EPUB books to bionic reading format
- Preserves the entire EPUB structure (chapters, sections, table of contents, images)
- Only text elements are processed, the rest of the content remains unchanged
- Supports both command-line interface and web interface
- Works with Unicode text, including Cyrillic characters

## Requirements

The following dependencies are required for the script to work:
```bash
ebooklib>=0.17.1
beautifulsoup4>=4.9.3
```

For the web interface (optional):
```bash
streamlit>=1.18.0
tqdm>=4.65.0
```

Install the dependencies using pip:
```bash
pip install -r requirements.txt
```

## Command-line Usage

Basic Usage:
```bash
python bionic_converter.py <path_to_epub_file> [save_path]
```

Arguments:
- `<path_to_epub_file>` - path to the source EPUB file (mandatory parameter)
- `[save_path]` - path for saving the converted file (optional)

If no save path is specified, the file will be saved in the same directory with the prefix `Bionic_` added to the file name.

## Web Interface

You can also use the web interface for more convenient file conversion:

```bash
streamlit run app.py
```

This will start a local web server and open a browser window with the interface where you can:
1. Upload an EPUB file
2. Convert it to bionic format
3. Download the resulting file

## Examples

File conversion with automatic result name:
```bash
python bionic_converter.py my_book.epub
```

This will create a file named `Bionic_my_book.epub` in the same directory.

Conversion with a specific output path:
```bash
python bionic_converter.py my_book.epub output/bionic_book.epub
```

## How It Works

The converter processes HTML content within the EPUB file and transforms the text by making the first half of each word bold. This creates a bionic reading effect that helps guide the eye through the text and can improve reading speed.

The conversion algorithm:
1. Loads the EPUB file
2. Processes each HTML document in the book
3. Finds all text nodes in paragraphs and headings
4. Applies bionic formatting to each word
5. Preserves original EPUB structure and metadata
6. Creates a new EPUB file with the processed content

## Running with the Shell Script

For convenience, you can also use the included shell script:

```bash
./run.sh 'my_book.epub'
```

This script activates the virtual environment (if present) and runs the converter.