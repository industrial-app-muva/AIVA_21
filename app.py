import base64
import io
import os

import cv2 as cv
import numpy as np
from PIL import Image

from flask import Flask, render_template, request, jsonify

from capacitor_detector.api import CapacitorDetectorAPI


UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
api = CapacitorDetectorAPI()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def np_array_2_uri(np_array):
    img = Image.fromarray(np_array.astype("uint8"))

    raw_bytes = io.BytesIO()
    img.save(raw_bytes, "JPEG")
    raw_bytes.seek(0)

    img_base64 = base64.b64encode(raw_bytes.getvalue()).decode('ascii')
    mime = "image/jpeg"
    uri = "data:%s;base64,%s" % (mime, img_base64)

    return uri


def parse_file_storage_2_numpy(file):
    # read image file string data
    file_str = file.read()
    # convert string data to numpy array
    np_img = np.frombuffer(file_str, np.uint8)
    # convert numpy array to image
    return cv.imdecode(np_img, cv.IMREAD_COLOR)


@app.route('/health-check')
def hello_world():
    return 'Online', 200


@app.route('/', methods=['GET', 'POST'])
def init_gui():
    return render_template('init.html')


@app.route('/process_img', methods=['POST'])
def process_img():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(error=400, text='Bad request'), 400

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '' or not file or not allowed_file(file.filename):
        return jsonify(error=400, text='Bad request'), 400

    im_input = parse_file_storage_2_numpy(file)
    _, bbox = api.process_img(im_input)

    return jsonify(bboxs=bbox)


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
        im_input = parse_file_storage_2_numpy(file)
        im_output, _ = api.process_img(im_input)

        im_input_uri = np_array_2_uri(im_input)
        im_output_uri = np_array_2_uri(im_output)

        return render_template('result.html', im_input=im_input_uri, im_output=im_output_uri)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

