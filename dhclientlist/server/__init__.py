#coding:utf-8
import os
try:
    from OpenSSL import SSL
    from security import generate_certificate, generate_key
    SECURITY_AVAILBLE = True
except ImportError:
    SECURITY_AVAILBLE = False


def serve(app, port, secure=True, debug=False):
    from werkzeug.serving import run_simple

    kwargs = {'host': '0.0.0.0',
              'port': int(port),
              'debug': debug}

    if secure and SECURITY_AVAILBLE:
        key_fd, key_fn, key = generate_key()
        cert_fd, cert_fn = generate_certificate(key)

        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_privatekey_file(key_fn)
        context.use_certificate_file(cert_fn)
        kwargs['ssl_context'] = context
    else:
        print "HTTPS server mode unavailble due to missing pyOpenSSL==0.13 library. Please install it to enable HTTPS server mode."

    run_simple(kwargs['host'], kwargs['port'], app, use_debugger=kwargs['debug'], use_reloader=True)

    if secure and SECURITY_AVAILBLE:
        os.close(cert_fd)
        os.remove(cert_fn)

        os.close(key_fd)
        os.remove(key_fn)
