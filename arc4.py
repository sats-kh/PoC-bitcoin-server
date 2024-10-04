import binascii

import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4  # Updated import path
from cryptography.hazmat.primitives.ciphers import Cipher
import base64

def init_arc4(seed):
    if isinstance(seed, str):
        seed = binascii.unhexlify(seed)
    backend = default_backend()
    cipher = Cipher(ARC4(seed), mode=None, backend=backend)  # nosec
    return cipher

def arc4_decrypt(key, cyphertext):
    """Un-obfuscate. initialize key once per attempt."""
    decryptor = key.decryptor()
    return decryptor.update(cyphertext) + decryptor.finalize()

def get_arc4_path():
    return ARC4.__module__

cipher = init_arc4("6005ee8cc02e528e20c8e5ff71191723b0260391020862a03587a985f813dabe")
a = arc4_decrypt(cipher, b'\xc4ks\xfe/\xf99\xbe\xa5\xd0\xa5w\x95\r\xc8\x87n\x86;\xed\x11\xc8\x87\xd6\x81A}\xfdpS>\x906\xc8\x18,pw\x0f\x8fk\xd7\x02\xa2\\qy\xbf\xff\x1c\xcb:\x84B\x97\xa7\x17"k\x88\xb9v')

key = b'`\x05\xee\x8c\xc0.R\x8e \xc8\xe5\xffq\x19\x17#\xb0&\x03\x91\x02\x08b\xa05\x87\xa9\x85\xf8\x13\xda\xbe'
somedata = b'stamp:{"p":"src-20","op":"transfer","tick":"STEVE","amt":"10}'
# test_pubkey = bytes.fromhex("0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798")
# hashed_pubkey = hashlib.sha256(test_pubkey).digest()
cipher = Cipher(ARC4(key), mode=None, backend=default_backend())
encryptor = cipher.encryptor()
encrypted = encryptor.update(somedata) + encryptor.finalize()

a = decrypted = arc4_decrypt(init_arc4(key), encrypted,)



b = '03c46b73fe2ff939bea5d0a577950dc8876e863bed11c887d681417dfd70533e51'


import zlib
