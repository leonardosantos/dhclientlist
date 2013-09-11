#coding:utf-8
from flask import Flask, request
from .auth import requires_auth
import json


def build(get_function, address, username, password, driver=None, http_username=None, http_password=None):
    app = Flask(__name__)

    @app.route("/")
    @requires_auth(http_username, http_password)
    def root():
        if request.args.get('format') == 'json':
            return json.dumps(get_function(address, username, password, driver))
        else:
            return 'Sorry, not implemented yet. Please append "?format=json" to your URL.'

    return app
