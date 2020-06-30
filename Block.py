from config import *
from HashAlgo import *


class Block:
    def __init__(self, prevBlockPtr, root, nonce, transactionList):
        self.prevBlockPtr = prevBlockPtr
        if(prevBlockPtr):
            self.prevBlockHash = prevBlockPtr.hashVal
        else:
            self.prevBlockHash = ""
        self.txnList = transactionList
        self.noOfTxn = len(transactionList)
        self.merkleTreeRoot = root
        self.nonce = nonce

        allHash = ""
        allHash += root.hashVal + self.prevBlockHash + str(nonce) + str(self.noOfTxn)
        self.hashVal = generateHash(allHash)
