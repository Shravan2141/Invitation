import sys
import os
import platform
import subprocess
import shutil

def check_python_environment():
    print("🐍 Python Environment Check 🐍")
    print("=" * 40)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Current Working Directory: {os.getcwd()}")

def check_dependencies():
    print("\n📦 Dependency Check 📦")
    print("=" * 40)
    
    dependencies = [
        'flask', 
        'opencv-python', 
        'numpy', 
        'gunicorn'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}: INSTALLED")
        except ImportError:
            print(f"❌ {dep}: NOT INSTALLED")
            try:
                print(f"Attempting to install {dep}...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
                print(f"✅ {dep}: Successfully installed")
            except Exception as e:
                print(f"❌ Failed to install {dep}: {e}")

def check_camera_access():
    print("\n📷 Camera Access Check 📷")
    print("=" * 40)
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Camera: Unable to access")
            print("Possible reasons:")
            print("- Camera is in use by another application")
            print("- No camera detected")
            print("- Camera drivers not installed")
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
            if 'templates' in file_path:
                print("   Hint: Recreate the templates directory and index.html")

def fix_virtual_environment():
    print("\n🔧 Virtual Environment Repair 🔧")
    print("=" * 40)
    
    venv_path = r'd:\Invitation\Invitation\src\venv'
    
    if os.path.exists(venv_path):
        try:
            shutil.rmtree(venv_path)
            print("✅ Removed existing virtual environment")
        except Exception as e:
            print(f"❌ Failed to remove virtual environment: {e}")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print("✅ Created new virtual environment")
        
        # Activate and install requirements
        activate_this = os.path.join(venv_path, 'Scripts', 'activate_this.py')
        exec(open(activate_this).read(), {'__file__': activate_this})
        
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', r'd:\Invitation\Invitation\src\requirements.txt'])
        print("✅ Installed project requirements")
    except Exception as e:
        print(f"❌ Virtual environment setup failed: {e}")

def main():
    print("🔍 COMPREHENSIVE TROUBLESHOOTING TOOL 🔍")
    print("=" * 50)
    
    check_python_environment()
    check_dependencies()
    check_camera_access()
    check_project_structure()
    fix_virtual_environment()

if __name__ == '__main__':
    main()
