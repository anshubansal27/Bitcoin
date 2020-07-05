from config import *
from HashAlgo import *

import sys


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
        # allHash += root.hashVal + self.prevBlockHash + str(nonce) + str(self.noOfTxn)
        allHash += self.prevBlockHash + str(nonce) + str(self.noOfTxn)
        self.hashVal = generateHash(allHash)

    def get_size(self):
        # print("prev ", self.hashVal , sys.getsizeof(self.prevBlockPtr))
        # print("txns ", len(self.hashVal) , sys.getsizeof(self.txnList))
        # totalSize = 0
        # print("type ", type(self.hashVal), len(self.hashVal.encode('utf-8')))
        # print("prev Block Hash",sys.getsizeof(self.prevBlockHash), sys.getsizeof(self.hashVal))
        # print("nonce size" , sys.getsizeof(self.nonce), self.nonce)
        print(" in 16.1")
        totalSize = 0
        totalSize += sys.getsizeof(self.prevBlockHash)
        totalSize += sys.getsizeof(self.nonce)
        totalSize += sys.getsizeof(self.hashVal)
        print(" in 16.2")
        for txn in self.txnList:
            # print(" in block get size txn")
            totalSize += txn.get_size()
        print(" in 16.3")
        # noOfNodesinMerkleTree = self.txnList
        # n = len(self.txnList)
        noOfNodesinMerkleTree = 15
        n = 15
        # print(" Block arity " , arity)
        while(n>1):
            noOfNodesinMerkleTree += (n + arity - 1)//arity
            n = (n+ arity - 1)//arity
        totalSize += noOfNodesinMerkleTree * sys.getsizeof(self.merkleTreeRoot.hashVal)
        print(" in 16.4")
        return totalSize




# b = None
# # print(sys.getsizeof(b))
# b1 = Block(None, None, 879796, [])
# # print(sys.getsizeof(b1))
# b2 = Block(b1,b1, 3000, [])
# b1.get_size()
# b2.get_size()
# print((9+3)//4)
