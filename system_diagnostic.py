import sys
import platform
import subprocess
import os

def check_system_requirements():
    print("🖥️ System Requirements Check 🖥️")
    print("=" * 40)
    
    # Python Version
    print(f"Python Version: {sys.version}")
    
    # Operating System
    print(f"Operating System: {platform.platform()}")
    
    # Processor Architecture
    print(f"Processor: {platform.processor()}")
    
    # Check Python executable
    print(f"Python Executable: {sys.executable}")

def check_project_dependencies():
    print("\n📦 Dependency Check 📦")
    print("=" * 40)
    
    required_packages = [
        'flask', 
        'opencv-python', 
        'numpy', 
        'gunicorn'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: Installed")
        except ImportError:
            print(f"❌ {package}: NOT INSTALLED")

def check_camera_access():
    print("\n📷 Camera Access Check 📷")
    print("=" * 40)
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Camera: Unable to access")
        else:
            print("✅ Camera: Accessible")
            cap.release()
    except Exception as e:
        print(f"❌ Camera Check Failed: {e}")

def check_project_structure():
    print("\n📂 Project Structure Check 📂")
    print("=" * 40)
    
    project_root = r'd:\Invitation\Invitation'
    expected_files = [
        'src\\app.py',
        'src\\face.py',
        'src\\requirements.txt',
        'src\\templates\\index.html',
        'Dockerfile',
        'run_project.ps1'
    ]
    
    for file_path in expected_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}: EXISTS")
        else:
            print(f"❌ {file_path}: MISSING")

def main():
    print("🔍 COMPREHENSIVE SYSTEM DIAGNOSTIC TOOL 🔍")
    print("=" * 50)
    
    check_system_requirements()
    check_project_dependencies()
    check_camera_access()
    check_project_structure()

if __name__ == '__main__':
    main()
