import os
from flask import Flask, request, render_template, send_from_directory
import cv2
import numpy as np
from PIL import Image
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'

# Create required directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def pencil_sketch(image_path, blur_value=21, canny_threshold=50):
    # Ensure blur value is odd
    blur_value = int(blur_value)
    if blur_value % 2 == 0:
        blur_value += 1

    # Read image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Create the negative invert
    inv = 255 - gray
    # Apply Gaussian blur with custom kernel size
    blurred = cv2.GaussianBlur(inv, (blur_value, blur_value), 0)
    # Invert the blurred image
    inv_blurred = 255 - blurred

    # Create pencil sketch
    sketch = cv2.divide(gray, inv_blurred, scale=256.0)



    # Enhance the sketch
    sketch = cv2.normalize(sketch, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    # Apply sharpening kernel for a crisper effect
    kernel = np.array([[0, -1, 0],
                      [-1, 5, -1],
                      [0, -1, 0]])
    sketch = cv2.filter2D(sketch, -1, kernel)

    return sketch

def pen_draw_style(image_path, blur_value=9, canny_threshold=20):
    # Ensure blur value is odd and at least 1
    blur_value = int(blur_value)
    if blur_value < 1:
        blur_value = 1
    if blur_value % 2 == 0:
        blur_value += 1

    # Read image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Use a small Gaussian blur to reduce noise but keep fine details
    blurred = cv2.GaussianBlur(gray, (blur_value, blur_value), 0)

    # Fine, sharp edge detection (like a fine pen)
    pen_edges = cv2.Canny(blurred, canny_threshold, canny_threshold * 4, apertureSize=3, L2gradient=True)

    # Invert for black lines on white
    pen_img = 255 - pen_edges

    # Optional: Slightly enhance contrast for a crisp ink look
    pen_img = cv2.normalize(pen_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

    return pen_img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    # Generate unique filename
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Get blur and canny values from form
    pencil_blur = request.form.get('pencilBlur', '21')
    pen_blur = request.form.get('mangaBlur', '9')
    # pencil_canny is ignored for pencil_sketch
    pen_canny = int(request.form.get('penCanny', '20'))

    # Generate both styles with custom blur and canny values
    sketch_img = pencil_sketch(filepath, pencil_blur)
    pen_img = pen_draw_style(filepath, pen_blur, pen_canny)

    # Save processed images
    sketch_filename = f'sketch_{filename}'
    pen_filename = f'pen_{filename}'
    
    cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'], sketch_filename), sketch_img)
    cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'], pen_filename), pen_img)

    return {
        'original': filename,
        'sketch': sketch_filename,
        'pen': pen_filename
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
