import sys
import os
import subprocess
import platform

def check_python_environment():
    print("Python Environment Check:")
    print("-" * 30)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Current Working Directory: {os.getcwd()}")
    print("\n")

def check_dependencies():
    print("Dependency Check:")
    print("-" * 30)
    dependencies = [
        'flask', 
        'opencv-python-headless', 
        'numpy', 
        'gunicorn'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"{dep}: INSTALLED ✓")
        except ImportError:
            print(f"{dep}: NOT INSTALLED ✗")
    print("\n")

def check_project_structure():
    print("Project Structure Check:")
    print("-" * 30)
    project_files = [
        'src/app.py',
        'src/face.py',
        'src/requirements.txt',
        'src/templates/index.html',
        'src/haarcascade_frontalface_default.xml'
    ]
    
    for file in project_files:
        if os.path.exists(file):
            print(f"{file}: EXISTS ✓")
        else:
            print(f"{file}: MISSING ✗")
    print("\n")

def test_flask_app():
    print("Flask Application Test:")
    print("-" * 30)
    try:
        import flask
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return "Test successful!"
        
        print("Flask initialization: SUCCESSFUL ✓")
    except Exception as e:
        print(f"Flask initialization FAILED: {e} ✗")
    print("\n")

def test_opencv():
    print("OpenCV Compatibility Test:")
    print("-" * 30)
    try:
        import cv2
        print(f"OpenCV Version: {cv2.__version__}")
        
        # Test basic face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        print("Haar Cascade Classifier: LOADED ✓")
    except Exception as e:
        print(f"OpenCV Test FAILED: {e} ✗")
    print("\n")

def install_dependencies():
    print("Attempting to Install Dependencies:")
    print("-" * 30)
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'src/requirements.txt'])
        print("Dependencies Installation: SUCCESSFUL ✓")
    except subprocess.CalledProcessError:
        print("Dependencies Installation: FAILED ✗")
    print("\n")

def main():
    print("🔍 COMPREHENSIVE PROJECT DIAGNOSTIC TOOL 🔍")
    print("=" * 50)
    
    check_python_environment()
    check_dependencies()
    check_project_structure()
    test_flask_app()
    test_opencv()
    install_dependencies()

if __name__ == '__main__':
    main()
