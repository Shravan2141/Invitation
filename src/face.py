import cv2
import numpy as np
import time
import webbrowser
import os
import ctypes

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

# Initialize face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Get screen dimensions
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Set window dimensions
window_width = 640
window_height = 480

# Calculate window position for center of screen
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2

# Create a named window and set it to be always on top
cv2.namedWindow('TECHKSHETRA 24', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('TECHKSHETRA 24', cv2.WND_PROP_TOPMOST, 1)
cv2.moveWindow('TECHKSHETRA 24', window_x, window_y)
cv2.resizeWindow('TECHKSHETRA 24', window_width, window_height)

# Start video capture
cap = cv2.VideoCapture(0)

# Set capture dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_height)

start_time = time.time()
detection_time = None
scanning_complete = False
face_detected = False

# Scanning animation parameters
scan_line_pos = 0
scan_direction = 1

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

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    # Check for timeout (20 seconds) if no face detected
    if not face_detected and elapsed_time >= 20:
        break
        
    ret, frame = cap.read()
    if not ret:
        break
        
    # Flip frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Create a copy of the frame for overlay effects
    display_frame = frame.copy()
    
    # Add tech border
    display_frame = draw_tech_border(display_frame)
    
    # Add scanning line effect if face not detected
    if not face_detected:
        cv2.line(display_frame, 
                 (0, scan_line_pos), 
                 (frame.shape[1], scan_line_pos), 
                 (0, 255, 255), 1)
        scan_line_pos += 5 * scan_direction
        if scan_line_pos >= frame.shape[0] or scan_line_pos <= 0:
            scan_direction *= -1
    
    # Draw rectangles around faces with cool effects
    for (x, y, w, h) in faces:
        if not face_detected:
            face_detected = True
            detection_time = current_time
            
        # Create targeting box effect
        cv2.rectangle(display_frame, (x-2, y-2), (x+w+2, y+h+2), (0, 255, 255), 1)
        cv2.rectangle(display_frame, (x-1, y-1), (x+w+1, y+h+1), (255, 255, 255), 1)
        
        # Add targeting lines
        cv2.line(display_frame, (x+w//2, 0), (x+w//2, y), (0, 255, 255), 1)
        cv2.line(display_frame, (x+w//2, y+h), (x+w//2, frame.shape[0]), (0, 255, 255), 1)
        cv2.line(display_frame, (0, y+h//2), (x, y+h//2), (0, 255, 255), 1)
        cv2.line(display_frame, (x+w, y+h//2), (frame.shape[1], y+h//2), (0, 255, 255), 1)
    
    # Add text overlays
    if not face_detected:
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
        time_since_detection = current_time - detection_time
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
    
    # Show the frame
    cv2.imshow('TECHKSHETRA 24', display_frame)
    
    # Check for window close button or 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('TECHKSHETRA 24', cv2.WND_PROP_VISIBLE) < 1:
        break

# Clean up
cap.release()
cv2.destroyAllWindows()

if face_detected:
    print("Face Detection Successful! Opening link...")
    # Open the link in default web browser
    url = "https://drive.google.com/file/d/1H5P4q7NQt3W7uYz62DTzYVx_Gx8XjxWy/view?usp=drivesdk"  # Replace with your desired URL
    webbrowser.open(url)
else:
    print("No face detected. Please try again.")
