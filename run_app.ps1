# Change to the src directory
cd "d:\Invitation\Invitation\src"

# Create virtual environment if not exists
if (-Not (Test-Path -Path "venv")) {
    python -m venv venv
}

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Run the Flask application
python app.py
