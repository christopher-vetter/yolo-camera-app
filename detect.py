from ultralytics import YOLO
import sys
import json

# Expect first CLI argument as image path
image_path = sys.argv[1]

# Load YOLO model (nano for speed)
model = YOLO("yolov8n.pt")

results = model.predict(source=image_path, imgsz=640, conf=0.25, verbose=False)

detections = []
for r in results:
    for box in r.boxes:
        detections.append({
            "class": model.names[int(box.cls)],
            "confidence": float(box.conf),
            "box": box.xyxy[0].tolist()
        })

print(json.dumps(detections))  # Send to Node.js
