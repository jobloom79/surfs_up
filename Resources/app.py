from cmath import exp
from flask import Flask
from sklearn.tree import export_graphviz
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello world!!!'

export FLASK_APP = app.py