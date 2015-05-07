import os
import sys
import json

sys.path.append(os.getcwd()+'/../')

from flask            import Flask, request, render_template, session, jsonify
from MrUirf           import main
from MrUirf.twitter   import collector_by_web
from MrUirf.facebook  import collector

app = Flask(__name__)
app.secret_key = "really_secret_key"

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
    data = get_texts(data)
    return render_template('uif/text.html', data=data)

@app.route('/uif/text/change_page')
def uif_text_change_page():
    data = {}
    data = get_texts_page(data)
    return jsonify(texts=data['texts'])

@app.route('/uif/token', methods=['GET', 'POST'])
def uif_token():
    data = {}
    data = get_texts(data)
    return render_template('uif/token.html', data=data)

@app.route('/uif/token/change_page')
def uif_token_change_page():
    data = {}
    data = get_texts_page(data)
    return jsonify(texts=data['texts'])

@app.route('/uif/extractor', methods=['GET', 'POST'])
def uif_extraction():
    data = {}
    if request.method == 'GET': 
        data['method'] = "GET"
        return render_template("uif/extractor.html", data=data)
    elif request.method == 'POST':
        data['method'] = 'POST'
        return render_template('uif/extractor.html', data=data)

def get_texts(data):
    session['host'] = request.url_root
    if request.method == 'GET':
        session['method'] = "GET"
        return render_template("uif/text.html", data=data)
    elif request.method == 'POST':
        session['method'] = 'POST'
        try:session['user_id'] = request.form['user_id']
        except:pass
        try:session['tw_page_no'] = request.form['tw_page_no']
        except:pass
        try:session['fb_page_no'] = request.form['fb_page_no']
        except:pass
        try:session['source'] = request.form['source']
        except:pass

        with file('tw_fb.account', 'r') as f:
            account_data = json.load(f)
        if session['source'] == "twitter":
            tw_username = account_data[session['user_id']]['tw_username']
            tw_page_no  = session['tw_page_no']
            data['texts']=collector_by_web.fetch_tweets(tw_username, tw_page_no)
        elif session['source'] == "facebook":
            fb_username = account_data[session['user_id']]['fb_username']
            fb_page_no  = session['fb_page_no']
            data['texts']=collector.fetch_status(fb_username, fb_page_no)
    return data

def get_texts_page(data):
    with file('tw_fb.account', 'r') as f:
        account_data = json.load(f)
    source = session['source']
    turn_pg= request.args.get('page', 0, type=str)
    if source == "twitter":
        tw_username  = account_data[session['user_id']]['tw_username']
        if turn_pg == "next":session['tw_page_no']=int(session['tw_page_no'])+1
        if turn_pg == "prev":session['tw_page_no']=int(session['tw_page_no'])-1
        tw_page_no = session['tw_page_no']
        data['texts']=collector_by_web.fetch_tweets(tw_username, tw_page_no)
    elif source == "facebook":
        fb_username  = account_data[session['user_id']]['fb_username']
        if turn_pg == "next":session['fb_page_no']=int(session['fb_page_no'])+1
        if turn_pg == "prev":session['fb_page_no']=int(session['fb_page_no'])-1
        fb_page_no = session['fb_page_no']
        data['texts']=collector.fetch_status(fb_username, fb_page_no)
    return data

