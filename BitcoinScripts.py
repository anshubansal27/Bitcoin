
class ScriptPubKey:

    def __init__(self, publicKeyHash):
        self.publicKeyHash = publicKeyHash

class ScriptSign:

    def __init__(self, sign, publickey):
        self.sign = sign
        self.pubKey = publickey


def executeScripts(scriptSign, ScriptPubKey):
    pass
