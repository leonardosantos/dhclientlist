#coding:utf-8
import os
from OpenSSL import SSL
from .security import generate_certificate, generate_key


def serve(app, port, secure=True, debug=False):
    kwargs = {'host': '0.0.0.0',
              'port': int(port),
              'debug': debug}

    if secure:
        key_fd, key_fn, key = generate_key()
        cert_fd, cert_fn = generate_certificate(key)

        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_privatekey_file(key_fn)
        context.use_certificate_file(cert_fn)
        kwargs['ssl_context'] = context

    app.run(**kwargs)

    if secure:
        os.close(cert_fd)
        os.remove(cert_fn)

        os.close(key_fd)
        os.remove(key_fn)
