#!/bin/sh

# Pull the latest updates from the remote repository
git pull

# Activate the virtual environment
source venv/bin/activate

# Run the Streamlit application
streamlit run SD3.py --server.port 8501
