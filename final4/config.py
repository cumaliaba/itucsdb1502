import os

from flask import Flask

UPLOAD_FOLDER = 'final4/uploads'

app = Flask(__name__)

# generate secret key
app.secret_key = os.urandom(32)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APP_FOLDER'] = 'final4'
