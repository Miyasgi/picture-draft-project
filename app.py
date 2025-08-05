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

def pencil_sketch(image_path, blur_value=21):
    # Ensure blur value is odd
    blur_value = int(blur_value)
    if blur_value % 2 == 0:
        blur_value += 1

    # Read image
    img = cv2.imread(image_path)
    # Convert to RGB for better color processing
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Convert to grayscale
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
    sketch = cv2.GaussianBlur(sketch, (3, 3), 0)
    sketch = cv2.addWeighted(sketch, 1.5, sketch, -0.5, 0)
    
    return sketch

def manga_style(image_path, blur_value=9):
    # Ensure blur value is odd
    blur_value = int(blur_value)
    if blur_value % 2 == 0:
        blur_value += 1

    # Read image
    img = cv2.imread(image_path)
    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Convert to grayscale
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    
    # Apply bilateral filter for edge preservation and noise reduction
    bilateral = cv2.bilateralFilter(gray, blur_value, 75, 75)
    
    # Create edge mask
    edges = cv2.Canny(bilateral, 100, 200)
    
    # Enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(bilateral)
    
    # Apply adaptive thresholding
    manga = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 11, 2)
    
    # Combine edges with manga style
    manga = cv2.addWeighted(manga, 0.7, edges, 0.3, 0)
    
    # Clean up noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    manga = cv2.morphologyEx(manga, cv2.MORPH_CLOSE, kernel)
    
    return manga

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

    # Get blur values from form
    pencil_blur = request.form.get('pencilBlur', '21')
    manga_blur = request.form.get('mangaBlur', '9')

    # Generate both styles with custom blur values
    sketch_img = pencil_sketch(filepath, pencil_blur)
    manga_img = manga_style(filepath, manga_blur)

    # Save processed images
    sketch_filename = f'sketch_{filename}'
    manga_filename = f'manga_{filename}'
    
    cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'], sketch_filename), sketch_img)
    cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'], manga_filename), manga_img)

    return {
        'original': filename,
        'sketch': sketch_filename,
        'manga': manga_filename
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
