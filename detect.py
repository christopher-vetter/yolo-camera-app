import sys
from ultralytics import YOLO
import os

if len(sys.argv) < 2:
    print("No image path provided")
    sys.exit(1)

image_path = sys.argv[1]

if not os.path.exists(image_path):
    print(f"Image not found: {image_path}")
    sys.exit(1)

# Load YOLO model (YOLOv8n for speed; change to yolov8s or yolov11 if available)
model = YOLO("yolov8n.pt")

# Run detection
results = model(image_path)

# Print detection results
for result in results:
    boxes = result.boxes
    names = result.names
    detections = []
    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        detections.append({
            "class": names[cls_id],
            "confidence": round(conf, 2)
        })
    print(detections)
