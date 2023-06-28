from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import os

current_image = None
color_analysis = None

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


class ColorAnalysis:

    def __init__(self, color1_hex, color1_rgb, color1_percent, color2_hex, color2_rgb, color2_percent, color3_hex,
                 color3_rgb, color3_percent,
                 color4_hex, color4_rgb, color4_percent, color5_hex, color5_rgb, color5_percent, color6_hex, color6_rgb,
                 color6_percent,
                 color7_hex, color7_rgb, color7_percent, color8_hex, color8_rgb, color8_percent, color9_hex, color9_rgb,
                 color9_percent,
                 color10_hex, color10_rgb, color10_percent):
        self.color1_hex = color1_hex
        self.color1_rgb = color1_rgb
        self.color1_percent = color1_percent
        self.color2_hex = color2_hex
        self.color2_rgb = color2_rgb
        self.color2_percent = color2_percent
        self.color3_hex = color3_hex
        self.color3_rgb = color3_rgb
        self.color3_percent = color3_percent
        self.color4_hex = color4_hex
        self.color4_rgb = color4_rgb
        self.color4_percent = color4_percent
        self.color5_hex = color5_hex
        self.color5_rgb = color5_rgb
        self.color5_percent = color5_percent
        self.color6_hex = color6_hex
        self.color6_rgb = color6_rgb
        self.color6_percent = color6_percent
        self.color7_hex = color7_hex
        self.color7_rgb = color7_rgb
        self.color7_percent = color7_percent
        self.color8_hex = color8_hex
        self.color8_rgb = color8_rgb
        self.color8_percent = color8_percent
        self.color9_hex = color9_hex
        self.color9_rgb = color9_rgb
        self.color9_percent = color9_percent
        self.color10_hex = color10_hex
        self.color10_rgb = color10_rgb
        self.color10_percent = color10_percent


def rgb2hex(rgb):
    return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))


def analyze_colors(file):
    global color_analysis
    image = Image.open(file)
    image = image.resize((50, 50))  # Reduce computation
    image_np = np.array(image)  # Convert image to numpy array
    image_np = image_np.reshape((-1, 3))  # Reshape to fit KMeans input

    # Apply KMeans to find the most dominant colors
    kmeans = KMeans(n_clusters=10)
    kmeans.fit(image_np)

    # Get colors
    colors = kmeans.cluster_centers_

    # Count the number of pixels in each cluster
    labels, counts = np.unique(kmeans.labels_, return_counts=True)

    color_percentages = counts / np.sum(counts)  # Get the percentage of each color

    # Get the indices that would sort color_percentages in descending order
    sorted_indices = np.argsort(color_percentages)[::-1]

    # Sort colors and color_percentages using the sorted_indices
    colors = colors[sorted_indices]
    color_percentages = color_percentages[sorted_indices]

    # Create a ColorAnalysis object
    color_analysis = ColorAnalysis(
        rgb2hex(colors[0]), colors[0], color_percentages[0],
        rgb2hex(colors[1]), colors[1], color_percentages[1],
        rgb2hex(colors[2]), colors[2], color_percentages[2],
        rgb2hex(colors[3]), colors[3], color_percentages[3],
        rgb2hex(colors[4]), colors[4], color_percentages[4],
        rgb2hex(colors[5]), colors[5], color_percentages[5],
        rgb2hex(colors[6]), colors[6], color_percentages[6],
        rgb2hex(colors[7]), colors[7], color_percentages[7],
        rgb2hex(colors[8]), colors[8], color_percentages[8],
        rgb2hex(colors[9]), colors[9], color_percentages[9]
    )

    return


@app.route("/")
def home():
    return render_template("index.html", image=current_image, color=color_analysis)


@app.route("/analyze", methods=["POST"])
def analyze():
    if 'file' not in request.files:
        flash('No file part')
        return redirect("/")
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect("/")
    if file:
        global current_image
        if current_image is not None:
            os.remove(current_image)
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.getcwd(), f"static/{filename}")
        file.save(file_path)
        analyze_colors(file_path)
        current_image = f"static/{filename}"
        flash('analysis_ready')
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
