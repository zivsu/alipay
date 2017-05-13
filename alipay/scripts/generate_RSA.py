import sys
import os.path

import sys
sys.path[0] = sys.path[0] + "/.."

from Crypto.PublicKey import RSA

import define
import config

key = RSA.generate(2048)
with open(config.private_key_path, "w") as fp:
    fp.write(key.exportKey('PEM'))

with open(config.public_key_path, "w") as fp:
    fp.write(key.publickey().exportKey("PEM"))