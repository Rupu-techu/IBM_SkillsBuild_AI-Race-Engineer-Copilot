#!/bin/bash

# Setup script for Streamlit deployment

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = \$PORT\n\
\n\
[theme]\n\
primaryColor = \"#e63946\"\n\
backgroundColor = \"#0a0a0a\"\n\
secondaryBackgroundColor = \"#1a1a2e\"\n\
textColor = \"#ffffff\"\n\
font = \"monospace\"\n\
" > ~/.streamlit/config.toml

# Made with Bob
