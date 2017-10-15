import sys

sys.path.insert(0, 'ml')

import logic.ml as mlogic
import logic.crawler as crawler
from flask import Flask, jsonify
from flask import request, render_template
from logic.url_tools import valid_url

app = Flask(__name__)

model = 'english'
model_path = 'saves/{}/save.model'.format(model)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify():
    url = request.form['url']
    if not valid_url(url): return make_error('Not valid url!')
    scrap_data = crawler.scrap_page(url)
    data = crawler.special_to_text(scrap_data)
    positive = mlogic.classify(data, model_path)
    return jsonify({
        'success': True,
        'positive': bool(positive),
        'preview': crawler.special_to_html(scrap_data)
    })


@app.route('/preview', methods=['POST'])
def preview():
    url = request.form['url']
    if not valid_url(url): return make_error('Not valid url!')
    return str(crawler.scrap_page(url))


def make_error(message):
    return jsonify({'success': False, 'message': message})
