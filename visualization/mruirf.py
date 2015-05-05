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

	error = ""

	if request.method == "POST":

		data = ','.join([request.form["depth"], request.form["iterations"], request.form["github_username"], request.form["twitter_username"]])

		main.start(request.form["github_username"], request.form["twitter_username"], request.form["depth"], request.form["iterations"])

		return data


