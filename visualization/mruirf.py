import os
import sys

sys.path.append(os.getcwd()+'/../')

from flask import Flask, request, render_template

from MrUirf import main

app = Flask(__name__)

@app.route('/')
def index():

	return render_template("index.html")

@app.route('/uir', methods=['POST'])
def uir():

    main.start("stamaimer", "stamaimer")


# --------------------------------------------------

@app.route('/uif')
def uif_index():
    return render_template("uif/index.html")

@app.route('/uif/extraction')
def uif_extraction():
    return render_template("uif/extraction.html")

