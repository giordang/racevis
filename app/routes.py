from app import app
from flask import render_template, redirect, url_for, request, flash

@app.route('/')
@app.route('/index')
def index():
    return render_template('upload.html')