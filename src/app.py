from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/run-face')
def run_face():
    try:
        # Get the absolute path to face.py
        script_path = os.path.join(os.path.dirname(__file__), 'face.py')
        
        # Run the face detection script using pythonw
        subprocess.Popen(['pythonw', script_path], 
                        creationflags=subprocess.CREATE_NO_WINDOW)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True)
