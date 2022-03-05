# Flask server for camera

from flask import Flask, render_template, request
import cv2, base64, io
import numpy as np
from PIL import Image
from threading import Thread

app = Flask(__name__)

current_img = None

def from_base64(base64_string):
    imgdata = base64.b64decode(str(base64_string[22:]))
    image = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_img
    if request.method == 'POST':
        current_img = from_base64(request.data.decode('utf-8'))
        return 'POST'
    return render_template('index.html')

def start():
    print("starting camera thread...")
    t = Thread(target=app.run)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    start()
    while True:
        pass