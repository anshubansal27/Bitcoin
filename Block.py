from config import *
from HashAlgo import *


class Block:
    def __init__(self, prevBlockPtr, root, nonce, transactionList):
        self.prevBlockPtr = prevBlockPtr
        self.prevBlockHash = prevBlockPtr.hashVal
        self.txnList = transactionList
        self.noOfTxn = len(transactionList)
        self.merkleTreeRoot = root
        self.nonce = nonce

        allHash = ""
        allHash += root.hashVal + prevBlockPtr.hashVal + str(nonce) + str(self.noOfTxn)
        self.hashVal = generateHash(allHash)

