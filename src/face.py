import cv2
import time
import webbrowser
import os

# Load the Haar Cascade Classifier for face detection
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)  # 0 is the default camera

start_time = time.time()  # Record the start time
face_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_classifier.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    # Draw bounding boxes around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
        face_detected = True

    # Display the frame with detected faces
    cv2.imshow("Face Detection", frame)

    # If face is detected and 5 seconds have passed
    if face_detected and (time.time() - start_time > 5):
        break

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the webcam window
cap.release()
cv2.destroyAllWindows()

if face_detected:
    print("Face Detection Successful! Opening link...")
    # Open the link in default web browser
    url = "https://vimeo.com/1057096601/41d6db1bd9"  # Replace with your desired URL
    webbrowser.open(url)
else:
    print("No face detected. Please try again.")
