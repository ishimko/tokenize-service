from flask import request
from flask import Flask
from flask import jsonify
import shelve
import uuid

app = Flask('tokenize-service')

BAD_REQUEST = '', 400
NOT_FOUND = '', 404

TEST_TOKEN = '11111111-2222-3333-4444-555555555555'
TEST_CARD = '4444333322221111'


@app.before_first_request
def initialize():
    with open_db() as db:
        if not db.get(TEST_TOKEN):
            db[TEST_TOKEN] = TEST_CARD


@app.route('/securestorage/<storage_type>', methods=['POST'])
def storeClearText(storage_type):
    if is_valid_storage_type(storage_type):
        if request.json:
            request_json = request.json
            clear_text = request_json['clearText']
            if clear_text:
                with open_db() as db:
                    token = str(uuid.uuid4())
                    db[token] = clear_text
                    response = { 'token': token }
                    return jsonify(response), 200
            else:
                return BAD_REQUEST
        else:
            return BAD_REQUEST
    else:
        return NOT_FOUND


@app.route('/securestorage/<storage_type>/<token>', methods=['GET'])
def getClearText(storage_type, token):
    if is_valid_storage_type(storage_type):
        if token:
            with open_db() as db:
                clear_text = db.get(token)
                if clear_text:
                    response = { 'clearText': clear_text }
                    return jsonify(response), 200
                else:
                    return NOT_FOUND
        else:
            return BAD_REQUEST
    else:
        return NOT_FOUND    


def open_db():
    return shelve.open(r'.\storage\db')


def is_valid_storage_type(storage_type):
    return storage_type.lower() == 'cardnumber'
