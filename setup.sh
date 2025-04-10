#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Check if pip is installed
if [ ! -d "venv" ]; then
    echo "# Create a virtual environment if one does not exist"
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Virtual Environment Activation..."
source venv/bin/activate

# Install dependenciesи
echo "Dependency Setup..."
pip install -r requirements.txt

# Make the scripts executable
echo "Setting permissions to execute scripts..."
chmod +x bionic_converter.py
chmod +x run.sh

# Design
echo ""
echo "====================================================="
echo "     Installation of EPUB Bionic Converter is complete!"
echo "====================================================="
echo ""
echo "You can use the converter in two ways:"
echo ""
echo "1. Command Line:"
echo "   ./run.sh '<path to the epub file' [save_path]"
echo ""
echo "   Example: ./run.sh 'My_book.epub'"
echo ""
echo "2. Web interface (more user-friendly):"
echo "   source venv/bin/activate  # Activate the environment if it is not already activated"
echo "   streamlit run app.py"
echo ""
echo "   After that, an interface will open in your browser where you can download the file,"
echo "   adjust the settings and download the result."
echo ""
echo "New Opportunities:"
echo " ✓ Cyrillic support"
echo " ✓ Dark theme with improved contrast"
echo " ✓ Web interface for easy use"
echo " ✓ Saving EPUB file structure"
echo ""
echo "To update the converter in the future, simply run setup.sh again."
echo "" 