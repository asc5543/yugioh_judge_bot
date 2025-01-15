from flask import Flask
from waitress import serve

import os

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def keep_alive():
    serve(app, host=os.environ['HOST'], port=int(os.environ['PORT']))