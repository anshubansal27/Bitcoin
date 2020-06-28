from config import *
class Block:
    def __init__(self, prevHash,root, nonce):
        self.prevHash = prevHash
        self.merkleTreeRoot = root
        self.nonce = nonce
        self.txnList = []
        return