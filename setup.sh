#!/bin/bash

# AI Regex Generator Setup Script

# Function to display messages
msg() {
    echo -e "\n\033[1;32m>>> $1\033[0m\n"
}

error() {
    echo -e "\n\033[1;31m>>> ERROR: $1\033[0m\n"
    exit 1
}

# Check Python version
msg "Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d ' ' -f 2)
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 8 ]); then
    error "Python 3.8+ is required. Found Python $python_version"
fi

echo "Python $python_version found. Proceeding with installation..."

# Create virtual environment
msg "Creating virtual environment..."
python3 -m venv venv || error "Failed to create virtual environment"
source venv/bin/activate || error "Failed to activate virtual environment"

# Upgrade pip
msg "Upgrading pip..."
pip install --upgrade pip || error "Failed to upgrade pip"

# Install dependencies
msg "Installing dependencies..."
pip install -r requirements.txt || error "Failed to install dependencies"

# Set up environment file
msg "Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template. Please edit it to add your OpenAI API key."
else
    echo ".env file already exists. Skipping..."
fi

# Create necessary directories
msg "Creating necessary directories..."
mkdir -p app/static/img

# Initialize database
msg "Initializing database..."
python -m scripts.init_db || error "Failed to initialize database"

# Success message
msg "Setup completed successfully!"
echo "To start the application, run: uvicorn main:app --reload"
echo "Then open http://localhost:8000 in your browser"
echo ""
echo "For more information, please refer to the README.md file."