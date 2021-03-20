import os
import cv2 as cv
import numpy as np

from flask import Flask, render_template, flash, request, url_for, abort
from werkzeug.utils import secure_filename, redirect

from capacitor_detector.api import CapacitorDetectorAPI


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = Flask(__name__)
api = CapacitorDetectorAPI()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_file_storage_2_numpy(file):
    # read image file string data
    file_str = file.read()
    # convert string data to numpy array
    np_img = np.fromstring(file_str, np.uint8)
    # convert numpy array to image
    return cv.imdecode(np_img, cv.IMREAD_COLOR)


@app.route('/health-check')
def hello_world():
    return 'Welcome to Capacitor Detector API'


@app.route('/', methods=['GET', 'POST'])
def init_gui():
    return render_template('init.html')


@app.route('/process_img_gui', methods=['POST'])
def process_img_gui():
    # check if the post request has the file part
    if 'file' not in request.files:
        return render_template('init.html', error='No file part')

    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return render_template('init.html', error='No selected file')

    if file and allowed_file(file.filename):
        img = parse_file_storage_2_numpy(file)

        # img, bboxs = api.process_img(img)
        return render_template('result.html', )




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)

