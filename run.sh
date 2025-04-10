#!/bin/bash

# Check if the virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual Environment Activation..."
    source venv/bin/activate
fi

# Run the converter with the passed arguments
python3 bionic_converter.py "$@" 