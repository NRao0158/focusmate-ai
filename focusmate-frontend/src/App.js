import React, { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";
import io from "socket.io-client";
import "./App.css";

const socket = io("http://localhost:5000", {
  transports: ["websocket", "polling"],
});

function App() {
  const webcamRef = useRef(null);
  const [isDistracted, setIsDistracted] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [frameCount, setFrameCount] = useState(0);

  useEffect(() => {
    socket.on("connect", () => {
      console.log("Connected to backend!");
      setIsConnected(true);
    });

    socket.on("disconnect", () => {
      setIsConnected(false);
    });

    // Listen for AI status from Python
    socket.on("focus_status", (data) => {
      setIsDistracted(data.distracted);
      setFrameCount((prev) => prev + 1);
    });

    // Send a frame every 200ms
    const interval = setInterval(() => {
      if (webcamRef.current) {
        const imageSrc = webcamRef.current.getScreenshot();
        if (imageSrc) {
          socket.emit("video_frame", imageSrc);
        }
      }
    }, 200);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      {/* Visual Blur Overlay */}
      <div className={isDistracted ? "blur-overlay active" : "blur-overlay"}>
        <div className="alert-box">
          <h1>⚠️ DISTRACTION DETECTED!</h1>
          <p>Please look back at your screen to resume.</p>
          {/* Dismiss button so you don't get stuck */}
          <button 
            className="dismiss-btn"
            onClick={() => setIsDistracted(false)}
          >
            Close / Dismiss (Manual Override)
          </button>
        </div>
      </div>

      <div className="dashboard">
        <h1>FocusMate Diagnostics</h1>

        <div className="status-container">
          <div className={`status-pill ${isConnected ? "online" : "offline"}`}>
            Backend: {isConnected ? "🟢 Connected" : "🔴 Disconnected"}
          </div>
          <div className={`status-pill ${isDistracted ? "distracted" : "focused"}`}>
            Status: {isDistracted ? "🚨 DISTRACTED" : "✅ FOCUSED"}
          </div>
          <div className="status-pill info">
            Updates Received: {frameCount}
          </div>
        </div>

        <div className="webcam-box">
          <h3>Camera Feed:</h3>
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            width={320}
            height={240}
          />
        </div>

        <button
          className="test-btn"
          onClick={() => setIsDistracted(!isDistracted)}
        >
          Test Screen Blur
        </button>
      </div>
    </div>
  );
}

export default App;