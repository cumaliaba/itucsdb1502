import os

from flask import Flask

app = Flask(__name__)

# generate secret key
app.secret_key = os.urandom(32)

app.config['APP_FOLDER'] = 'final4'
