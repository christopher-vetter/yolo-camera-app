import torch
import cv2

# Load model once globally
model = torch.hub.load('ultralytics/yolov5', 'yolov8.pt', pretrained=True)  # or yolov8

def run_detection(img):
    results = model(img)
    labels = results.pandas().xyxy[0]['name'].tolist()

    annotated_img = results.render()[0]

    return labels, annotated_img
