#coding:utf-8
import werkzeug
import json
from  .. import util


def build(get_function, address, username, password, driver=None, http_username=None, http_password=None):
    def app(environ, start_response):
        request = werkzeug.Request(environ)
        auth = werkzeug.http.parse_authorization_header(request.headers.get('Authorization', ''))
        if (not http_username and not http_password) or (auth and auth.username == http_username and auth.password == http_password):
            result = get_function(address, username, password, driver)
            if request.args.get('format') == 'json':
                response = werkzeug.Response(json.dumps(result), headers={'Content-Type': 'application/json'})
            else:
                response = werkzeug.Response(util.to_texttable(result))
        else:
            response = werkzeug.Response('Could not verify your access level for that URL.\n'
                                         'You have to login with proper credentials',
                                         401, {'WWW-Authenticate': 'Basic'})
        return response(environ, start_response)
    return app
