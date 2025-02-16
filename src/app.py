from flask import Flask, render_template, Response, send_from_directory
import cv2
import numpy as np
import time
import webbrowser
import os
import ctypes
import threading
import subprocess

app = Flask(__name__)

# Reuse the face detection logic from face.py
def create_overlay_text(frame, text, position, font_scale=0.7, thickness=2):
    font = cv2.FONT_HERSHEY_DUPLEX
    # Get text size
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Create semi-transparent overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, 
                 (position[0] - 10, position[1] - text_height - 10),
                 (position[0] + text_width + 10, position[1] + 10),
                 (0, 0, 0), -1)
    
    # Add text
    cv2.putText(overlay, text, position, font, font_scale, (0, 255, 255), thickness)
    
    # Blend the overlay with the original frame
    alpha = 0.7
    return cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

def create_success_animation(frame, progress):
    height, width = frame.shape[:2]
    overlay = frame.copy()
    
    # Create circular animation
    center = (width // 2, height // 2)
    radius = int(min(width, height) * 0.8 * progress)
    cv2.circle(overlay, center, radius, (0, 255, 255), 2)
    
    # Add success lines
    if progress > 0.5:
        line_progress = (progress - 0.5) * 2  # Scale from 0 to 1
        # Draw checkmark or success indicator
        start_point = (width // 2 - 40, height // 2)
        mid_point = (width // 2 - 10, height // 2 + 30)
        end_point = (width // 2 + 40, height // 2 - 20)
        
        # Calculate points based on progress
        mid_x = int(start_point[0] + (mid_point[0] - start_point[0]) * line_progress)
        mid_y = int(start_point[1] + (mid_point[1] - start_point[1]) * line_progress)
        end_x = int(mid_point[0] + (end_point[0] - mid_point[0]) * line_progress)
        end_y = int(mid_point[1] + (end_point[1] - mid_point[1]) * line_progress)
        
        cv2.line(overlay, start_point, (mid_x, mid_y), (0, 255, 255), 2)
        if progress > 0.75:
            cv2.line(overlay, mid_point, (end_x, end_y), (0, 255, 255), 2)
    
    return cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)

def draw_tech_border(frame):
    h, w = frame.shape[:2]
    border_color = (0, 255, 255)  # Yellow color
    thickness = 2
    
    # Draw tech corners
    corner_length = 30
    gap = 5
    
    # Top-left
    cv2.line(frame, (gap, gap), (corner_length, gap), border_color, thickness)
    cv2.line(frame, (gap, gap), (gap, corner_length), border_color, thickness)
    
    # Top-right
    cv2.line(frame, (w-gap, gap), (w-corner_length, gap), border_color, thickness)
    cv2.line(frame, (w-gap, gap), (w-gap, corner_length), border_color, thickness)
    
    # Bottom-left
    cv2.line(frame, (gap, h-gap), (corner_length, h-gap), border_color, thickness)
    cv2.line(frame, (gap, h-gap), (gap, h-corner_length), border_color, thickness)
    
    # Bottom-right
    cv2.line(frame, (w-gap, h-gap), (w-corner_length, h-gap), border_color, thickness)
    cv2.line(frame, (w-gap, h-gap), (w-gap, h-corner_length), border_color, thickness)
    
    return frame

class FaceDetection:
    def __init__(self):
        # Initialize face detection and camera early
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Add CAP_DSHOW for faster initialization on Windows

        # Set window dimensions
        self.window_width = 640
        self.window_height = 480

        # Set capture dimensions immediately
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.window_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.window_height)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffer delay

        self.start_time = time.time()
        self.detection_time = None
        self.scanning_complete = False
        self.face_detected = False

        # Scanning animation parameters
        self.scan_line_pos = 0
        self.scan_direction = 1

    def generate_frames(self):
        while True:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            
            # Check for timeout (20 seconds) if no face detected
            if not self.face_detected and elapsed_time >= 20:
                break
                
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Flip frame horizontally for a mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Create a copy of the frame for overlay effects
            display_frame = frame.copy()
            
            # Add tech border
            display_frame = draw_tech_border(display_frame)
            
            # Add scanning line effect if face not detected
            if not self.face_detected:
                cv2.line(display_frame, 
                         (0, self.scan_line_pos), 
                         (frame.shape[1], self.scan_line_pos), 
                         (0, 255, 255), 1)
                self.scan_line_pos += 5 * self.scan_direction
                if self.scan_line_pos >= frame.shape[0] or self.scan_line_pos <= 0:
                    self.scan_direction *= -1
            
            # Draw rectangles around faces with cool effects
            for (x, y, w, h) in faces:
                if not self.face_detected:
                    self.face_detected = True
                    self.detection_time = current_time
                    
                # Create targeting box effect
                cv2.rectangle(display_frame, (x-2, y-2), (x+w+2, y+h+2), (0, 255, 255), 1)
                cv2.rectangle(display_frame, (x-1, y-1), (x+w+1, y+h+1), (255, 255, 255), 1)
                
                # Add targeting lines
                cv2.line(display_frame, (x+w//2, 0), (x+w//2, y), (0, 255, 255), 1)
                cv2.line(display_frame, (x+w//2, y+h), (x+w//2, frame.shape[0]), (0, 255, 255), 1)
                cv2.line(display_frame, (0, y+h//2), (x, y+h//2), (0, 255, 255), 1)
                cv2.line(display_frame, (x+w, y+h//2), (frame.shape[1], y+h//2), (0, 255, 255), 1)
            
            # Add text overlays
            if not self.face_detected:
                display_frame = create_overlay_text(display_frame, 
                                                  "INITIALIZING FACE SCAN...", 
                                                  (20, 30))
                display_frame = create_overlay_text(display_frame,
                                                  "AWAITING GUEST VERIFICATION",
                                                  (20, 60))
                # Show remaining time
                remaining_time = max(0, 20 - elapsed_time)
                display_frame = create_overlay_text(display_frame,
                                                  f"TIMEOUT IN: {remaining_time:.1f}s",
                                                  (20, 90))
            else:
                time_since_detection = current_time - self.detection_time
                if time_since_detection <= 2.0:
                    # Create success animation
                    animation_progress = min(time_since_detection / 2.0, 1.0)
                    display_frame = create_success_animation(display_frame, animation_progress)
                    
                    display_frame = create_overlay_text(display_frame, 
                                                      "TARGET ACQUIRED!", 
                                                      (20, 30))
                    display_frame = create_overlay_text(display_frame,
                                                      "GUEST VERIFICATION COMPLETE",
                                                      (20, 60))
                else:
                    break
            
            # Add timestamp
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            display_frame = create_overlay_text(display_frame,
                                              f"TIME: {timestamp}",
                                              (20, frame.shape[0]-20))
            
            # Encode frame for streaming
            ret, buffer = cv2.imencode('.jpg', display_frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def release(self):
        self.cap.release()

# Global face detection instance
face_detector = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/face')
def face():
    global face_detector
    face_detector = FaceDetection()
    return render_template('face_detection.html')

@app.route('/video_feed')
def video_feed():
    global face_detector
    if face_detector:
        return Response(face_detector.generate_frames(), 
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return "Camera not initialized", 400

@app.route('/check_detection')
def check_detection():
    global face_detector
    if face_detector and face_detector.face_detected:
        # Open the link
        target_url = "https://drive.google.com/file/d/1H5P4q7NQt3W7uYz62DTzYVx_Gx8XjxWy/view?usp=drivesdk"
        return {"status": "success", "url": target_url}
    return {"status": "waiting"}

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
    
    app.run(host='0.0.0.0', port=5000, debug=True)
