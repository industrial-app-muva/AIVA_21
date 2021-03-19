from flask import Flask
from capacitor_detector.api import CapacitorDetectorAPI
app = Flask(__name__)

api = CapacitorDetectorAPI()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/process_img', methods=['POST'])
def process_img():
    # TODO: Parse request
    #       Validar imagen
    img, bboxs = api.process_img(img)
    # TODO: Parse results
    #       Return results
    pass