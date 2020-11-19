import os
from app import app
from flask import render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
#import functions

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'gpx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/index')
def index():
    clear_folder()
    return render_template('upload.html')


@app.route('/process', methods=['POST'])
def process():
    clear_folder()

    if 'file' in request.files:
        print('file')
    else:
        print('nope')
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #functions.doSomeStuff(filename)

    return render_template('results.html')


def clear_folder():
    folder = 'uploads'

    filelist = [ f for f in os.listdir(folder) if f.endswith(".gpx") ]
    for f in filelist:
        os.remove(os.path.join(folder, f))