import os
import json
import cv2

# Load the local face detection model
model_file = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(model_file)

if face_cascade.empty():
    raise SystemExit("Error: haarcascade_frontalface_default.xml not found.")

def evaluate_folder(folder_path, expect_face=True):
    total = 0
    correct = 0
    failures = []

    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith((".jpg", ".png")):
            continue

        total += 1
        filepath = os.path.join(folder_path, filename)
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Exact parameters used in production
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=4, 
            minSize=(40, 40)
        )

        face_detected = (len(faces) > 0)

        # Ground truth evaluation
        if expect_face and face_detected:
            correct += 1
        elif not expect_face and not face_detected:
            correct += 1
        else:
            failures.append({
                "file": filename,
                "expected_face": expect_face,
                "detected_faces": len(faces)
            })

    return total, correct, failures

# Run benchmark across both classes
total_focused, correct_focused, fn_failures = evaluate_folder("dataset/focused", expect_face=True)
total_distracted, correct_distracted, fp_failures = evaluate_folder("dataset/distracted", expect_face=False)

total_samples = total_focused + total_distracted
total_correct = correct_focused + correct_distracted
accuracy = (total_correct / total_samples) * 100

report = {
    "model": "OpenCV Haar Cascade (haarcascade_frontalface_default)",
    "parameters": {
        "scaleFactor": 1.1,
        "minNeighbors": 4,
        "minSize": [40, 40]
    },
    "metrics": {
        "total_test_frames": total_samples,
        "correct_predictions": total_correct,
        "accuracy_percentage": round(accuracy, 2),
        "false_negatives": len(fn_failures), # Face was there, but missed (e.g., low light/glasses)
        "false_positives": len(fp_failures)  # False detection when looking away
    },
    "failure_cases": {
        "false_negatives": fn_failures,
        "false_positives": fp_failures
    }
}

# Print clean terminal report
print("\n" + "="*50)
print("       FOCUSMATE DETECTION BENCHMARK REPORT       ")
print("="*50)
print(f"Total Evaluation Frames : {total_samples}")
print(f"Correct Predictions     : {total_correct}/{total_samples}")
print(f"Model Accuracy          : {accuracy:.2f}%")
print(f"False Negatives (Missed): {len(fn_failures)}")
print(f"False Positives (Ghosts): {len(fp_failures)}")
print("="*50)

# Save report to JSON
with open("benchmark_report.json", "w") as f:
    json.dump(report, f, indent=4)

print("📁 Detailed report exported to: benchmark_report.json\n")