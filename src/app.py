from flask import Flask, render_template, Response, jsonify
import cv2
import os
import sys
import logging
import traceback
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app_log.txt'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')

def generate_frames():
    try:
        # Ensure OpenCV can find Haar cascade file
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            logging.error(f"Haar cascade file not found: {cascade_path}")
            return

        face_cascade = cv2.CascadeClassifier(cascade_path)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            logging.error("Unable to open camera")
            return

        while True:
            success, frame = cap.read()
            if not success:
                logging.warning("Failed to capture frame")
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()
    except Exception as e:
        logging.error(f"Error in generate_frames: {e}")
        logging.error(traceback.format_exc())
        yield b''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run-face')
def run_face():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'face.py')
        result = subprocess.run(
            [sys.executable, script_path], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            return jsonify({"status": "success", "output": result.stdout})
        else:
            logging.error(f"Face script error: {result.stderr}")
            return jsonify({"status": "error", "message": result.stderr})
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Script timed out"})
    except Exception as e:
        logging.error(f"Error running face script: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled Exception: {e}")
    logging.error(traceback.format_exc())
    return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Ensure necessary directories exist
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    logging.info("Starting Flask Application...")
    logging.info(f"Python Version: {sys.version}")
    logging.info(f"OpenCV Version: {cv2.__version__}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
