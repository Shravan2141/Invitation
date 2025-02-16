# Invitation Face Detection App

## Local Development Setup

### Prerequisites
- Python 3.9+
- pip
- virtualenv

### Installation Steps
1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows: `.\venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`
5. Install dependencies:
   ```
   pip install -r src/requirements.txt
   ```
6. Run the application:
   ```
   python src/app.py
   ```

## Deployment on Render

### Deployment Steps
1. Create a Render account
2. Connect your GitHub repository
3. Create a new Web Service
4. Select Docker deployment
5. Set build command: `docker build -t invitation-app .`
6. Set start command: `docker run -p 5000:5000 invitation-app`

## Features
- Real-time face detection
- Web-based video streaming
- Simple and intuitive interface

## Technologies
- Flask
- OpenCV
- Python
- Docker

## Troubleshooting
- Ensure all dependencies are installed
- Check camera permissions
- Verify Python and pip versions