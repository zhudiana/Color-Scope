Color Palette Generator (CPG)

This is a simple web application built with Flask that generates a color palette from an uploaded image. The app uses clustering algorithms to extract dominant colors and displays the colors along with their hex codes and percentage contributions. You can upload an image, and the app will generate a palette based on the image's colors.
Features

    Upload an image and generate a color palette.

    Displays dominant colors along with their RGB and HEX values.

    Shows the percentage of each color in the image.

    Optimized performance with image downscaling and pixel sampling.

Technologies

    Flask - Web framework for building the application.

    Pillow - Python Imaging Library for image processing.

    NumPy - For numerical operations.

    SciPy - For clustering and whitening.

    Matplotlib - For reading image files.

    HTML/CSS - For front-end display.

Installation
1. Clone the repository:

git clone https://github.com/zhudiana/Color-Paletter-Generator.git    
cd CPG

2. Set up a virtual environment:

For Linux/macOS:

python3 -m venv venv
source venv/bin/activate

For Windows:

python -m venv venv
.\venv\Scripts\activate

3. Install dependencies

4. Run the app:

python app.py

This will start a development server on http://127.0.0.1:5000/.
How It Works

    The user uploads an image via the form on the home page.

    The image is resized and processed by clustering the pixels to find dominant colors using the K-means algorithm.

    The app returns the color palette consisting of dominant colors, displaying the RGB and HEX values and their percentages in the image.

Features Explained

    Image Resizing: The image is downscaled to a maximum size of 800x800 pixels to optimize processing time.

    Pixel Sampling: Instead of processing all pixels, the app samples every 10th pixel to reduce computational load.

    Clustering: The app uses K-means clustering to identify the dominant colors and group similar colors together.

    Percentage Calculation: The app calculates the percentage of each dominant color relative to the total image.

Usage

    Navigate to the application in your browser.

    Click on the "Upload Your Own Image" button and select an image file from your computer.

    After uploading, the color palette will be displayed with the hex codes and percentage contributions of the colors in the image.
