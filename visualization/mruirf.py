import os
import sys
import json

sys.path.append(os.getcwd()+'/../')

from flask            import Flask, request, render_template, session, jsonify
from MrUirf           import main
from MrUirf.twitter   import collector_by_web
from MrUirf.facebook  import collector
from MrUirf.extraction.util import relextractor_map
from MrUirf.extraction.util import fusion

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
    if request.method == 'GET':session['method']='GET'
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
    if request.method == 'GET':session['method']='GET'
    data = {}
    data = get_texts(data)
    return render_template('uif/token.html', data=data)

@app.route('/uif/token/change_page')
def uif_token_change_page():
    data = {}
    data = get_texts_page(data)
    return jsonify(texts=data['texts'])

@app.route('/uif/pos', methods=['GET', 'POST'])
def uif_pos():
    if request.method == 'GET':session['method']='GET'
    data = {}
    if request.method == "POST":
        data = get_texts(data)
        texts= data['texts']
        for text in texts:
            pos = text['pos']
            pos = [(p[0], relextractor_map.convert_pos(p[1])) for p in pos]
            text['pos'] = pos
        data['texts'] = texts
    return render_template('uif/pos.html', data=data)

@app.route('/uif/pos/change_page')
def uif_pos_change_page():
    data = {}
    data = get_texts_page(data)
    texts= data['texts']
    for text in texts:
        pos = text['pos']
        pos = [(p[0], relextractor_map.convert_pos(p[1])) for p in pos]
        text['pos'] = pos
    data['texts'] = texts
    return jsonify(texts=data['texts'])

@app.route('/uif/extractor', methods=['GET', 'POST'])
def uif_extraction():
    if request.method == 'GET': session['method']='GET'
    data = {}
    data = get_texts(data)
    data = extractor_preprocess(data)
    return render_template('uif/extractor.html', data=data)

@app.route('/uif/extractor/change_page')
def uif_extraction_change_page():
    data = {}
    data = get_texts_page(data)
    data = extractor_preprocess(data)
    return jsonify(texts=data['texts'])

@app.route('/uif/complement', methods=['GET', 'POST'])
def uif_complement():
    data = {}
    if request.method == 'GET': session['method']='GET'
    elif request.method=='POST':
        session['method']='POST'
        data = get_entities(data)
    return render_template('uif/complement.html', data=data)

@app.route('/uif/complement/change_page')
def uif_complement_change_page():
    data = {}
    data = get_entities_page(data)
    return jsonify(entities=data['entities'])

def extractor_preprocess(data):
    if session['method'] == 'GET': return data
    texts= data['texts']
    for text in texts:
        tokens = text['tokens']
        entity_relevance = {}
        for entity in text['entity']:
            word = entity['word']
            rele = entity['relevance']
            rele_indice = []
            for key in rele:
                for rele_word in rele[key]:
                    rele_indice.append(str(tokens.index(rele_word)))
            try:entity_relevance[tokens.index(word)]=" ".join(rele_indice)
            except:pass
        text['entity_relevance'] = entity_relevance
        text['tokens'] = [(i, w) for i, w in enumerate(tokens)]
    data['texts'] = texts
    return data

def get_entities(data):
    session['host'] = request.url_root
    if request.method == 'GET':
        session['method'] = 'GET'
    if request.method == 'POST':
        session['method'] = 'POST'
        try:
            session['user_id'] = request.form['user_id']
            session['mc_page_no'] = request.form['mc_page_no']
            session['tw_page_no'] = request.form['tw_page_no']
            session['fb_page_no'] = request.form['fb_page_no']
        except:pass
        session['mode'] = request.form['mode']

        user_id = session['user_id']
        mode    = session['mode']
        if   mode=='0': page_no = session['mc_page_no']
        elif mode=='1': page_no = session['tw_page_no']
        elif mode=='2': page_no = session['fb_page_no']
        entities = fusion.get_entities(user_id, mode, page_no)
        data['entities'] = entities
    return data

def get_entities_page(data):
    turn_pg = request.args.get('page', 0, type=str)
    user_id = session['user_id']
    mode    = session['mode']
    if   mode=='0': page_no = session['mc_page_no']
    elif mode=='1': page_no = session['tw_page_no']
    elif mode=='2': page_no = session['fb_page_no']
    if turn_pg == "next": page_no = int(page_no)+1
    if turn_pg == "prev": page_no = int(page_no)-1
    if   mode=='0': session['mc_page_no'] = page_no
    elif mode=='1': session['tw_page_no'] = page_no
    elif mode=='2': session['fb_page_no'] = page_no
    entities = fusion.get_entities(user_id, mode, page_no)
    data['entities'] = entities
    return data

def get_texts(data):
    session['host'] = request.url_root
    if request.method == 'GET':
        session['method'] = 'GET'
        return render_template("uif/text.html", data=data)
    if request.method == 'POST':
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

def get_raw_text(data):
    with file('tw_fb.account', 'r') as f:
        account_data = json.load(f)
    user_id= session['user_id']
    source = request.args.get('source', 0, type=str)
    source = source.replace("'", '"')
    source = source.replace('u"','"')
    source = json.loads(source)
    if source['sns'] == 'twitter':
        tw_username = account_data[user_id]['tw_username']
        index = source['index']
        data['text'] = collector_by_web.fetch_raw_tweet(tw_username, index)
    elif source['sns']=='facebook':
        fb_username = account_data[user_id]['fb_username']
        index = source['index']
        data['text'] = collector.fetch_raw_status(fb_username, index)
    return data
