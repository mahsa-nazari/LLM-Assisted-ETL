#!/bin/bash


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


echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi


source venv/bin/activate
echo "Virtual environment activated."


echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt


echo "Creating necessary directories..."
if [ ! -d "uploads" ]; then
    mkdir uploads
    echo "Uploads directory created."
fi


LOG_FILE="app.log"
if [ ! -f "$LOG_FILE" ]; then
    touch "$LOG_FILE"
    echo "Log file created at $LOG_FILE."
else
    echo "Log file already exists at $LOG_FILE."
fi


export FLASK_APP=app/dashboard.py  
export FLASK_ENV=development

echo "Flask environment variables set."


echo "Starting the Flask dashboard..."
flask run
