#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages
pip install regex beautifulsoup4 lxml tqdm

# Create requirements.txt file if it doesn't exist
if [ ! -f requirements.txt ]; then
  echo "Creating requirements.txt file"
  echo "regex" > requirements.txt
  echo "beautifulsoup4" >> requirements.txt
  echo "lxml" >> requirements.txt
  echo "tqdm" >> requirements.txt
fi

echo "Setup complete! Use 'source venv/bin/activate' to activate the virtual environment."
