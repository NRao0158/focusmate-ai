import os
import time
import cv2

# Create dataset directories
os.makedirs("dataset/focused", exist_ok=True)
os.makedirs("dataset/distracted", exist_ok=True)

cap = cv2.VideoCapture(0)

def capture_frames(label, count=100, delay=0.1):
    print(f"\n📸 GET READY: Capturing {count} frames for '{label}'...")
    print("Starting in 3 seconds. Vary your distance, lighting, and angles slightly!")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    saved = 0
    while saved < count:
        ret, frame = cap.read()
        if not ret:
            continue
        
        filepath = f"dataset/{label}/{label}_{saved+1:03d}.jpg"
        cv2.imwrite(filepath, frame)
        saved += 1
        
        # Show capture feed
        cv2.putText(frame, f"Capturing {label}: {saved}/{count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Data Collector", frame)
        
        if cv2.waitKey(int(delay * 1000)) & 0xFF == ord('q'):
            break
            
    print(f"✅ Finished capturing {saved} frames for '{label}'!")

# 1. Capture 100 Focused frames (look at the screen, adjust angles, blink, tilt)
input("Press ENTER to start capturing FOCUSED frames (look at camera/screen)...")
capture_frames("focused", count=100)

# 2. Capture 100 Distracted frames (look away >45 deg, look down at phone, turn off light)
input("\nPress ENTER to start capturing DISTRACTED frames (look away, turn head, look down)...")
capture_frames("distracted", count=100)

cap.release()
cv2.destroyAllWindows()
print("\n🎉 Dataset collection complete! 200 frames saved in ./dataset/")