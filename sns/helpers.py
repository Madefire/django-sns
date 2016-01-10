import requests

from M2Crypto import X509
from base64 import b64decode

certs = {}


def verify_signature(keys, message):
    # get public key
    url = message['SigningCertURL']
    if url not in certs:
        r = requests.get(url)
        cert_string = r.text
        certs[url] = cert_string
    else:
        cert_string = certs[url]
    cert = X509.load_cert_string(str(cert_string))
    pub_key = cert.get_pubkey()
    pub_key.reset_context(md='sha1')
    pub_key.verify_init()

    # create string to sign
    lines = []
    for key in keys:
        if key in message:
            lines.append(key)
            lines.append(message[key])
    str_to_sign = '\n'.join(lines)
    pub_key.verify_update(str_to_sign.encode())
    result = pub_key.verify_final(b64decode(message['Signature']))
    return result == 1
