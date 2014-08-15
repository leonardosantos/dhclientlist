#coding:utf-8
import os


def serve(app, port, debug=False):
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', int(port), app, use_debugger=debug, use_reloader=False)
