# Bionic Read

A tool to convert standard text to bionic reading format in EPUB files.

## Setup

This project uses a virtual environment to manage dependencies. To set it up:

```bash
# Create and activate the virtual environment
bash setup.sh
```

```bash
# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Once the environment is activated, you can run the converter:

```bash
python src/converter.py input.epub output.epub
```

## Requirements

- Python 3.6+
- regex
- beautifulsoup4
- lxml
- tqdm

## Development

To add more dependencies, add them to requirements.txt and run:

```bash
pip install -r requirements.txt
```