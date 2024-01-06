from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
import json
from json import JSONEncoder
import warnings
warnings.filterwarnings("ignore")
from werkzeug.utils import secure_filename
import os
from tensorflow.keras.models import model_from_json
import cv2
import numpy as np

app = Flask (__name__)

UPLOAD_FOLDER = 'C:\\Users\\shris\\Downloads\\Garbage-Classification\\uploads'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}
classes = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html', res=None)

@app.route('/upload', methods = ['GET','POST'])
def func():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            json_file = open('C:\\Users\\shris\\Downloads\\Garbage-Classification\\model\\model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model = model_from_json(loaded_model_json)
            model.load_weights("C:\\Users\\shris\\Downloads\\Garbage-Classification\\model\\model.h5")
            img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img2 = cv2.resize(img, (224, 224), interpolation = cv2.INTER_AREA)
            print(img2.shape)
            pred = np.round(model.predict(np.array([img2])))[0]
            print(pred)
            index = 0
            for i in range(len(pred)):
                if pred[i] == 1:
                    index = i
                    break
            print(index)
            return render_template('index.html', res=classes[index])
            
    return render_template('index.html', error="Error! Please Try Again")
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=False)