import os
import sys

sys.path.append(os.getcwd()+'/../')

from flask import Flask, request, render_template, session

from MrUirf import main

app = Flask(__name__)

@app.route('/')
def index():

	return render_template("index.html")

@app.route('/uir', methods=['POST'])
def uir():

	error = ""

	if request.method == "POST":

		results = main.start(request.form["github_username"],   
							 request.form["twitter_username"], 
							 int(request.form["depth"]),        
							 int(request.form["iterations"]))

		return render_template("results.html", results=results)

@app.route('/uif')
def uif_index():
    return render_template("uif/index.html")

@app.route('/uif/text', methods=['GET', 'POST'])
def uif_text():
    data = {}
    if request.method == 'GET': 
        data['method'] = "GET"
        return render_template("uif/text.html", data=data)
    elif request.method == 'POST':
        data['method'] = 'POST'
        data['page_count'] = request.form['page_count']
        data['source'] = request.form['source']
        return render_template('uif/text.html', data=data)


@app.route('/uif/extractor', methods=['GET', 'POST'])
def uif_extraction():
    data = {}
    if request.method == 'GET': 
        data['method'] = "GET"
        return render_template("uif/extractor.html", data=data)
    elif request.method == 'POST':
        data['method'] = 'POST'
        return render_template('uif/extractor.html', data=data)
