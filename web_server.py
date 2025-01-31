from flask import Flask
from threading import Thread
from waitress import serve

import os

app = Flask(__name__)

def run_in_develop():
    app.run(host=os.environ['HOST'], port=int(os.environ['PORT']))

def run_in_prod():
    serve(app, host=os.environ['HOST'], port=int(os.environ['PORT']))

def run(env: str = "prod"):
    if env == "prod":
        t = Thread(target=run_in_prod)
    else:
        t = Thread(target=run_in_develop)
    t.start()