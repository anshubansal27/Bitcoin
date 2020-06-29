import hashlib
from Crypto.PublicKey import RSA
# from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Signature.PKCS1_v1_5 import PKCS115_SigScheme
from Crypto.Hash import SHA256
class ScriptPubKey:

    def __init__(self, publicKeyHash):
        self.publicKeyHash = publicKeyHash

class ScriptSign:

    def __init__(self, sign, publickey):
        self.sign = sign
        self.pubKey = publickey


def executeScripts(scriptSign, ScriptPubKey):
    signature = scriptSign.sign
    sigPubKey = scriptSign.pubKey
    pubKeyHash = ScriptPubKey.publicKeyHash
    genpubKeyHash = SHA256.new(hashlib.sha256(sigPubKey).hexdigest().encode())
    # print(genpubKeyHash.hexdigest())
    if(pubKeyHash.hexdigest() != genpubKeyHash.hexdigest()):
        return False
    verifier = PKCS115_SigScheme(RSA.importKey(sigPubKey))
    try:
        verifier.verify(pubKeyHash, signature)
    except:
        return False
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
    
