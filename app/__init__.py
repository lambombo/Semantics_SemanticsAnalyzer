import os

from flask import Flask, Blueprint, request, jsonify, make_response
from config import config
from textblob import TextBlob

def get_sentiment(text):
    data = TextBlob(text)
    return data.sentiment.polarity

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize flask extensions

    # Register API routes
    @app.route('/', methods=['POST','GET'])
    def main():
        if request.method == 'GET':
            data = {"status":"ok"}
            return jsonify(data=data), 200
        if request.method == 'POST':
            try:
                json_data = request.get_json()
                text = json_data['body']
                print(text)
                data = get_sentiment(text)
                print(data)
                return make_response(jsonify(data = data), 200) 
            except Exception as e:
                data = dict(error = 'Unable to process request')
                return make_response(jsonify(data = data), 200)
        return jsonify(data = {"status":"ok"}), 200
        
    return app
