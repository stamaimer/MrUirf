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

		# if os.path.isfile("./static/data/gihub.json"):

		# 	os.remove("./static/data/gihub.json")

		# if os.path.isfile("./static/data/twitter.json"):

		# 	os.remove("./static/data/twitter.json")

		results = main.start(request.form["github_username"],   
							 request.form["twitter_username"], 
							 int(request.form["depth"]),        
							 int(request.form["iterations"]))

		return render_template("results.html", results=results)

@app.route('/uif')
def uif_index():
    return render_template("uif/index.html")

@app.route('/uif/extraction/<username>')
def uif_extraction(username = None):
    username = username
    return render_template("uif/extraction.html", username=username)
