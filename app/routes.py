import os
from app import app
from flask import render_template, redirect, url_for, request, flash, Markup
from werkzeug.utils import secure_filename
from app.functions import vis

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
        f = request.files['file']
        if (allowed_file(f.filename)):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = vis.vis_fun(filename)
            clear_folder()
            return render_template('results.html', data=data)
        else:
            print('wrong file type')
            return render_template('upload.html')
    else:
        print('no file uploaded')
        return render_template('upload.html')


@app.route('/map')
def mapbox_js():
    return render_template(
        'map.html', 
        ACCESS_KEY='pk.eyJ1IjoiZ3JlZ2dpb3IiLCJhIjoiY2todGlkbDcxMTJmcDJ4bWpmcmtkaTc3ciJ9.j5X2rKGeWuPYXETXGwoTKw'
    )


def clear_folder():
    folder = 'uploads'

    filelist = [ f for f in os.listdir(folder) if f.endswith(".gpx") ]
    for f in filelist:
        os.remove(os.path.join(folder, f))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS