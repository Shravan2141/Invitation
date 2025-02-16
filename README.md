# Invitation Face Detection Web App

## Project Overview
A web application for face detection using Flask and OpenCV, designed for the Techkshetra event.

## Features
- Interactive web interface
- Face detection functionality
- Docker and Render deployment support

## Local Development Setup

### Prerequisites
- Python 3.9+
- Docker (optional)

### Installation Steps
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r src/requirements.txt
   ```
4. Run the application:
   ```bash
   python src/app.py
   ```

## Docker Deployment

### Build Docker Image
```bash
docker build -t invitation-app .
```

### Run Docker Container
```bash
docker run -p 5000:5000 invitation-app
```

## Render Deployment
1. Fork the repository
2. Connect to Render
3. Select "Web Service"
4. Choose Docker runtime
5. Deploy

## Troubleshooting
- Ensure camera permissions are granted
- Check OpenCV dependencies
- Verify Python version compatibility

## Technologies
- Flask
- OpenCV
- Docker
- Render

## License
Open-source project