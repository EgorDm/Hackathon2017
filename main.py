import sys
sys.path.insert(0, 'ml')

import logic.ml as mlogic
from flask import Flask, jsonify
from flask import request,render_template
from logic.url_tools import valid_url


app = Flask(__name__)

model_path = 'saves/my_model/save.model'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classify', methods=['POST'])
def classify():
    url = request.form['url']
    if not valid_url(url): return make_error('Not valid url!')
    # TODO: scrap from this url
    data = 'We are sittig here at the hackathon doing koekeloeren and we still have 12 hours to go.'
    positive = mlogic.classify(data, model_path)
    return jsonify({
        'success': True,
        'positive': True
    })



def make_error(message):
    return jsonify({'success': False, 'message': message})
