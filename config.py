import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'topsecret'
    #UPLOAD_FOLDER = 'uploads'
    #ALLOWED_EXTENSIONS = {'gpx'}


