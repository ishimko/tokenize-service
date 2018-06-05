from flask import request
from flask import Flask
from flask import jsonify
import shelve
import uuid

app = Flask('tokenize-service')

BAD_REQUEST = '', 400

@app.route('/store', methods=['POST'])
def storeClearText():
    if request.json:
        request_json = request.json
        clear_text = request_json['text']
        if clear_text:
            with open_db() as db:
                token = str(uuid.uuid4())
                db[token] = clear_text
                response = {
                    'token': token
                }
                return jsonify(response), 201
        else:
            return BAD_REQUEST
    else:
        return BAD_REQUEST


@app.route('/get/<token>', methods=['GET'])
def getClearText(token):
    if token:
        with open_db() as db:
            clear_text = db.get(token)
            if clear_text:
                response = {
                    'clearText': clear_text
                }
                return jsonify(response), 200
            else:
                return BAD_REQUEST
    else:
        return BAD_REQUEST


def open_db():
    return shelve.open('db')
