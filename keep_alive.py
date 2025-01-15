from flask import Flask
from threading import Thread

import os

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host=os.environ['HOST'], port=int(os.environ['PORT']))

def keep_alive():
    t = Thread(target=run)
    t.start()