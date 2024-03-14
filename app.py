from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect_faces():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Read image
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Save the image with rectangles drawn around faces
    cv2.imwrite('static/result.jpg', img)

    return jsonify({'result_image': 'static/result.jpg'})

if __name__ == '__main__':
    app.run(debug=True)
