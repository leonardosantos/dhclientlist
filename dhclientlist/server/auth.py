#coding:utf-8
from functools import wraps
from flask import request, Response
from .settings import *


def requires_auth(http_username=None, http_password=None):
    if None in (http_username, http_password):
        return lambda _f: _f

    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not (auth.username == http_username and auth.password == http_password):
                return Response('Could not verify your access level for that URL.\n'
                                'You have to login with proper credentials', 401,
                                {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return f(*args, **kwargs)
        return decorated
    return wrapper
