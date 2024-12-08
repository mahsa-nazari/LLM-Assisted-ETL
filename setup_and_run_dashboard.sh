#!/bin/bash

# Step 1: Ensure Python and pip are installed
echo "Checking for Python and pip..."
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

if ! command -v pip3 &>/dev/null; then
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

echo "Python and pip are installed."

# Step 2: Set up virtual environment
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Step 3: Activate virtual environment
source venv/bin/activate
echo "Virtual environment activated."

# Step 4: Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Create necessary directories
echo "Creating necessary directories..."
if [ ! -d "uploads" ]; then
    mkdir uploads
    echo "Uploads directory created."
fi

# Step 6: Set up log file
LOG_FILE="app.log"
if [ ! -f "$LOG_FILE" ]; then
    touch "$LOG_FILE"
    echo "Log file created at $LOG_FILE."
else
    echo "Log file already exists at $LOG_FILE."
fi

# Step 7: Set Flask environment variables
export FLASK_APP=dashboard.py
export FLASK_ENV=development

echo "Flask environment variables set."

# Step 8: Run the Flask app
echo "Starting the Flask dashboard..."
flask run
