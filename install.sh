#!/bin/bash

# Check if the virtual environment folder exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt
python -m pip install --upgrade pip

# Deactivate the virtual environment
deactivate
exit
