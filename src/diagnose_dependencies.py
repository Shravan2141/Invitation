import sys
import platform

def check_dependencies():
    print("Python Version:", sys.version)
    print("Platform:", platform.platform())
    
    try:
        import flask
        print("Flask Version:", flask.__version__)
    except ImportError:
        print("Flask not installed")
    
    try:
        import cv2
        print("OpenCV Version:", cv2.__version__)
    except ImportError:
        print("OpenCV not installed")
    
    try:
        import numpy
        print("NumPy Version:", numpy.__version__)
    except ImportError:
        print("NumPy not installed")
    
    try:
        import PIL
        print("Pillow Version:", PIL.__version__)
    except ImportError:
        print("Pillow not installed")

if __name__ == "__main__":
    check_dependencies()
