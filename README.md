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

### Local Development

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

### Docker Deployment

1. Clone the repository and navigate to it:
```bash
git clone https://github.com/Miyasgi/picture-draft-project.git
cd picture-draft-project
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d --build
```

3. Access the application at `http://localhost:5000`

To stop the application:
```bash
docker-compose down
```

### Cloud Deployment

#### Prerequisites
- Docker installed on your cloud server
- Git installed on your cloud server
- Open port 5000 in your cloud server's firewall/security group

#### Deployment Steps

1. SSH into your cloud server:
```bash
ssh username@your-server-ip
```

2. Clone and deploy the application:
```bash
git clone https://github.com/Miyasgi/picture-draft-project.git
cd picture-draft-project
docker-compose up -d --build
```

3. Access the application at `http://your-server-ip:5000`

For production deployment, it's recommended to:
- Set up a domain name
- Configure SSL/TLS with Let's Encrypt
- Use a reverse proxy (like Nginx)
- Set up proper monitoring and logging

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