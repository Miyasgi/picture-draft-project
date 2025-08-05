# Picture Style Generator

A web application that transforms images into pencil sketches and manga-style artwork. Built with Flask and OpenCV.

## Features

- Upload high-resolution images
- Generate pencil sketch and manga-style versions
- Real-time adjustments with interactive sliders
- Custom blur effects for both styles
- Responsive web interface

## Technologies Used

- Backend: Python, Flask
- Image Processing: OpenCV, NumPy
- Frontend: HTML, CSS, JavaScript
- Image Handling: PIL (Python Imaging Library)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Miyasgi/picture-draft-project.git
cd picture-draft-project
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit `http://localhost:5000`

## Usage

1. Click "Choose File" to select an image
2. Click "Upload Image" to process the image
3. Use the sliders to adjust:
   - Pencil Sketch Blur: Controls the softness of the sketch effect
   - Manga Style Blur: Adjusts the detail level of the manga effect
4. Changes are applied in real-time as you move the sliders

## License

MIT License

## Author

[Miyasgi](https://github.com/Miyasgi)