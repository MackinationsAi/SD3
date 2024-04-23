#!/bin/sh

# Check if the virtual environment folder exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip3 install -r requirements.txt
python3 -m pip install --upgrade pip

# Deactivate the virtual environment
deactivate
exit
