#coding:utf-8
from socket import gethostname
import time

CERT_C = "BR"
CERT_ST = "Rio de Janeiro"
CERT_L = "Rio de Janeiro"
CERT_O = "INOA"
CERT_OU = "INOA"
CERT_SERIAL = int(time.time())
CERT_CN = gethostname()
CERT_NOT_BEFORE = 0
CERT_NOT_AFTER = 10*365*24*60*60

PKEY_BITS = 1024
