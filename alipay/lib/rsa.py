# coding=utf-8
from base64 import decodestring as decodebytes
from base64 import encodestring as encodebytes

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA, SHA256
from Crypto.PublicKey import RSA as PublicKeyRSA


class RSA(object):
    def __init__(self, key_path, sign_type="RSA2"):
        self.key_path = key_path
        self.sign_type = sign_type

    def gen_digest(self, message):
        """Generate a digest for signature

        Args:
            message (btye str): The next chunk of the message being hashed.
        Returns:
            a fresh instance of the hash object
        """
        return SHA.new(message) if self.sign_type == "RSA" else SHA256.new(message)

    def gen_signer(self):
        """Generate a signer.

        Returns:
            A signature scheme `PKCS115_SigScheme` object.
        """
        with open(self.key_path, "r") as fp:
            key = PublicKeyRSA.importKey(fp.read())
        return PKCS1_v1_5.new(key)

    def sign(self, message, charset="utf-8"):
        """Generate the PKCS#1 v1.5 signature of a message.

        Args:
            message (str): The next chunk of the message being hashed.
            charset (str, optional): Use to encode `message`, default is `utf-8`.
        Returns:
            The signature encoded as a string.
        """
        message = message.encode(charset)
        digest = self.gen_digest(message)
        signer = self.gen_signer()
        signature = signer.sign(digest)

        return remove_spec(encodebytes(signature).decode(charset))

    def verify(self, message, signature, charset="utf-8"):
        """Verify that a certain PKCS#1 v1.5 signature is authentic.

        Args:
            message (str): The next chunk of the message being hashed.
            signature(str): The signature that needs to be validated.
            charset (str, optional): Use to encode `message`, default is `utf-8`.
        Returns:
            True if verification is correct. False otherwise.
        """
        digest = self.gen_digest(message.encode(charset))
        signature = decodebytes(signature.encode(charset))
        signer = self.gen_signer()

        return signer.verify(digest, signature)

def remove_spec(t):
    """Remove white spaces, tabs, and new lines from a string"""
    for c in ['\n', '\t', ' ']:
        t = t.replace(c,'')
    return t