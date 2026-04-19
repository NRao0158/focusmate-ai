# FocusMate 🧠👁️

[![React](https://img.shields.io/badge/React-18.x-blue?logo=react)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.x-yellow?logo=python)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-SocketIO-black?logo=flask)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An accessible, real-time computer vision study tool engineered to mitigate executive dysfunction and attention drift in students with ADHD.

---

## 📌 Architecture Overview

FocusMate operates on a low-latency, full-duplex client-server pipeline:
- **Client (React.js):** Captures high-frame-rate webcam video streams and passes base64 JPEG buffers across WebSockets. Conditionally triggers hardware-accelerated CSS `backdrop-filter` overlays upon distraction events.
- **Backend (Flask-SocketIO):** Ingests frames and runs real-time facial landmark classification via OpenCV Haar feature-based cascades.
- **Trigger Engine:** Algorithmic state manager that flags sustained gaze-deviation intervals and broadcasts reactive state signals back to the DOM.

```text
[ React Frontend ]  --- (Base64 JPEG Streams) ---> [ Flask WebSocket Server ]
         ^                                                      |
         |                                            [ OpenCV Haar Cascade ]
         |                                                      |
  (CSS Blur Trigger) <--- (State: Distracted/Focused) <---------+
  ```

---

## ⚡ Tech Stack

- **Frontend:** React.js, WebSockets (`socket.io-client`), React-Webcam, CSS3 Backdrop Filter
- **Backend:** Python, Flask, Flask-SocketIO
- **Computer Vision:** OpenCV (`cv2`)
- **Prototyping & UX:** Figma

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js v18+

### 2. Backend Setup
```bash
pip install -r requirements.txt
python app.py
```

### 3. Frontend Setup
```bash
cd focusmate-frontend
npm install
npm start
```