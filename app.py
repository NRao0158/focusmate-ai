import os
import urllib.request
import base64
import cv2
import numpy as np
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 1. Automatically download the missing face model if you don't have it
model_file = "haarcascade_frontalface_default.xml"
if not os.path.exists(model_file):
    print("⏳ Downloading missing face detection model from OpenCV...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, model_file)
    print("✅ Model downloaded successfully!")

# 2. Load the model from your local project folder
face_cascade = cv2.CascadeClassifier(model_file)

if face_cascade.empty():
    print("❌ ERROR: Could not load face detection XML!")
else:
    print("✅ SUCCESS: OpenCV Face Detector is loaded and ACTIVE!")

@socketio.on('connect')
def handle_connect():
    print(">>> SUCCESS: React connected to Python backend! <<<")

@socketio.on('video_frame')
def handle_frame(data):
    try:
        if not data or ',' not in data:
            return

        header, encoded = data.split(',', 1)
        img_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=4, 
            minSize=(40, 40)
        )

        distracted = (len(faces) == 0)

        # Print live status to terminal
        if distracted:
            print("🚨 STATUS: DISTRACTED (No face found)")
        else:
            print(f"👀 STATUS: FOCUSED ({len(faces)} face detected)")

        emit('focus_status', {'distracted': distracted})

    except Exception as e:
        print(f"Error inside handle_frame: {e}")

if __name__ == '__main__':
    print("Backend starting on http://127.0.0.1:5000 ...")
    socketio.run(app, port=5000, debug=True)