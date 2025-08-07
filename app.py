from flask import Flask, request, jsonify
import base64
import torch
import cv2
import numpy as np
from detect import run_detection

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'No image field found'}), 400

    try:
        image_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        label, annotated_img = run_detection(img)

        _, buffer = cv2.imencode('.jpg', annotated_img)
        encoded_result = base64.b64encode(buffer).decode('utf-8')

        return jsonify({'label': label, 'image': encoded_result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "YOLO Camera API is running!"

if __name__ == '__main__':
    app.run(debug=True)
