import hashlib

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
# from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Signature.PKCS1_v1_5 import PKCS115_SigScheme


class ScriptPubKey:

    def __init__(self, publicKeyHash):
        self.publicKeyHash = publicKeyHash

class ScriptSign:

    def __init__(self, sign, publickey):
        self.sign = sign
        self.pubKey = publickey


def executeScripts(scriptSign, scriptPubKey):
    print("##### 5.2")
    signature = scriptSign.sign
    print("##### 5.3")
    sigPubKey = scriptSign.pubKey
    print("##### 5.4")
    pubKeyHash = scriptPubKey.publicKeyHash

    print("##### 5.5")
    genpubKeyHash = SHA256.new(hashlib.sha256(sigPubKey).hexdigest().encode())
    print("#### 7")
    # print(genpubKeyHash.hexdigest())
    if(pubKeyHash.hexdigest() != genpubKeyHash.hexdigest()):
        print("#### 7.1")
        return False
    verifier = PKCS115_SigScheme(RSA.importKey(sigPubKey))
    try:
        print("#### 7.2")
        verifier.verify(pubKeyHash, signature)
    except:
        return False
    print("#### 8")
    return True



# key = RSA.generate(2048)
# pubKey = key.publickey().exportKey('PEM')
# pvtKey = key.exportKey('PEM')
# hash = SHA256.new(hashlib.sha256(pubKey).hexdigest().encode())
# # print(hash.hexdigest())
# signer = PKCS115_SigScheme(RSA.importKey(pvtKey))
# signature = signer.sign(hash)
# key2 = RSA.generate(2048)
# pubKey2 = key2.publickey().exportKey('PEM')
# hash2 = SHA256.new(hashlib.sha256(pubKey2).hexdigest().encode())
# s = ScriptSign(signature, pubKey)
# scrptp = ScriptPubKey(hash2)
# print(executeScripts(s,scrptp))
