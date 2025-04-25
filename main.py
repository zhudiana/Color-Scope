import os
from flask import Flask, render_template, request
import matplotlib.image as img
import pandas as pd
from scipy.cluster.vq import whiten, kmeans, vq
import numpy as np
from datetime import datetime
from flask import render_template
from PIL import Image  # Import Pillow for image resizing

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Convert 0-255 RGB to HEX
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# Downscale image function
def downscale_image(image_path, max_size=(800, 800)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)  # Resize image to fit within the max size
        return np.array(img)

def process_cluster(center, stds):
    red_scaled, green_scaled, blue_scaled = center
    rgb = (
        int(red_scaled * stds['red']),
        int(green_scaled * stds['green']),
        int(blue_scaled * stds['blue'])
    )
    hex_code = rgb_to_hex(rgb)
    return rgb, hex_code

@app.route("/")
def hello_world():
    return render_template('index.html', year=datetime.now().year)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No image part", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    if file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        image_url = f"/static/uploads/{filename}"

        # Downscale the image
        image = downscale_image(f'.{image_url}')

        # Sampling pixels (sampling 10% of pixels)
        sampled_pixels = image[::10, ::10]  # Take every 10th pixel
        r, g, b = [], [], []

        for row in sampled_pixels:
            for pixel in row:
                if len(pixel) == 4:  # RGBA
                    temp_r, temp_g, temp_b, _ = pixel
                else:
                    temp_r, temp_g, temp_b = pixel
                r.append(temp_r)
                g.append(temp_g)
                b.append(temp_b)

        # Process colors as before
        image_df = pd.DataFrame({'red': r, 'green': g, 'blue': b})
        image_df['scaled_red'] = whiten(image_df['red'])
        image_df['scaled_green'] = whiten(image_df['green'])
        image_df['scaled_blue'] = whiten(image_df['blue'])

        # Clustering
        cluster_centers, _ = kmeans(image_df[['scaled_red', 'scaled_green', 'scaled_blue']], 10)  # Reduce number of clusters
        cluster_indices, _ = vq(image_df[['scaled_red', 'scaled_green', 'scaled_blue']], cluster_centers)

        # Percentages
        counts = np.bincount(cluster_indices)
        percentages = counts / counts.sum() * 100

        red_std, green_std, blue_std = image_df[['red', 'green', 'blue']].std()
        stds = {'red': red_std, 'green': green_std, 'blue': blue_std}

        color_data = []
        for i, center in enumerate(cluster_centers):
            rgb, hex_code = process_cluster(center, stds)
            color_data.append({
                'rgb': rgb,
                'hex': hex_code,
                'percentage': round(percentages[i], 2)
            })

        # Sort by percentage (optional)
        color_data = sorted(color_data, key=lambda x: -x['percentage'])

        return render_template("index.html", image_url=image_url, colors=color_data)

    return "Something went wrong", 500

if __name__ == "__main__":
    app.run(debug=True)
