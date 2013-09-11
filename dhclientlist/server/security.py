#coding:utf-8
from OpenSSL import crypto
from .settings import *
import tempfile


def generate_certificate(key):
    file_descriptor, filename = tempfile.mkstemp()

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = CERT_C
    cert.get_subject().ST = CERT_ST
    cert.get_subject().L = CERT_L
    cert.get_subject().O = CERT_O
    cert.get_subject().OU = CERT_OU
    cert.get_subject().CN = CERT_CN
    cert.set_serial_number(CERT_SERIAL)
    cert.gmtime_adj_notBefore(CERT_NOT_BEFORE)
    cert.gmtime_adj_notAfter(CERT_NOT_AFTER)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha1')

    cert_file = open(filename, "wt")
    cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    cert_file.close()

    return file_descriptor, filename


def generate_key():
    file_descriptor, filename = tempfile.mkstemp()

    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, PKEY_BITS)

    key_file = open(filename, "wt")
    key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    key_file.close()

    return file_descriptor, filename, k
