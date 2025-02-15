from flask import Flask, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__, template_folder='.', static_folder='static')

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/run-face')
def run_face():
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        face_script = os.path.join(script_dir, 'face.py')
        
        # Run pythonw.exe (windowless Python) to hide the console
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        subprocess.Popen(['pythonw', face_script], 
                        startupinfo=startupinfo,
                        creationflags=subprocess.CREATE_NO_WINDOW)
        return '', 204
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True)
