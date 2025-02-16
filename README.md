# TECHKSHETRA 25 Face Detection Web App

## Overview
This is a web-based face detection application that provides a futuristic, tech-inspired user interface for guest verification.

## Features
- Real-time face detection using browser's MediaDevices API
- Animated scanning and targeting effects
- Automatic link opening upon successful face detection

## Prerequisites
- Modern web browser with camera support
- Python 3.8+
- Flask

## Setup and Installation
1. Clone the repository
2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies
   ```bash
   pip install -r src/requirements.txt
   ```

## Running the Application
```bash
python src/app.py
```

## Usage
1. Grant camera permissions when prompted
2. Position your face in the camera view
3. Wait for face detection (max 20 seconds)
4. Upon successful detection, the app will automatically open a link

## Technologies
- Python
- Flask
- JavaScript
- HTML5 Canvas
- MediaDevices API

## License
[Your License Here]