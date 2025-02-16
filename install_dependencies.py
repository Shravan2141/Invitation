import os
import sys
import subprocess

def install_dependencies():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to requirements.txt
    requirements_path = os.path.join(script_dir, 'src', 'requirements.txt')
    
    print(f"Script Directory: {script_dir}")
    print(f"Requirements Path: {requirements_path}")
    
    # Verify requirements file exists
    if not os.path.exists(requirements_path):
        print(f"ERROR: Requirements file not found at {requirements_path}")
        return False
    
    # Create virtual environment if it doesn't exist
    venv_path = os.path.join(script_dir, 'src', 'venv')
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
    
    # Activate virtual environment
    activate_this = os.path.join(venv_path, 'Scripts', 'activate_this.py')
    exec(open(activate_this).read(), {'__file__': activate_this})
    
    # Upgrade pip
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    
    # Install requirements
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def main():
    print("🔧 Dependency Installation Tool 🔧")
    print("=" * 40)
    
    # Detailed system information
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Working Directory: {os.getcwd()}")
    
    success = install_dependencies()
    
    if success:
        print("\n✅ Installation completed successfully!")
    else:
        print("\n❌ Installation encountered issues.")

if __name__ == '__main__':
    main()
