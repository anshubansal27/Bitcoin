from Crypto.PublicKey import RSA
from config import *
from random import randrange
from MerkleTree import MerkleTree
from Transaction import *

class Node:
    def __init__(self):
        key = RSA.generate(2048)
        self.pubKey = key.publickey().exportKey('PEM')
        self.pvtKey = key.exportKey('PEM')
        self.transactions = []
        self.blockqueue = []
        self.target = None
        self.utxo = 25
        self.incentive = 0

    def generateNonce(self):
        return randrange(0,2**sizeOfNonce)

    
    def generateBlock(self):
        
        return

    def generateMerkleTree(self):
        count = 0
        childs = []
        for i in self.transactions:
            childs.append((MerkleTree([i],True),0))
        while(len(childs) > 1):
            level = childs[0][1]
            merkleTreeChild = []
            for i in range(arity):
                if(len(childs) > 0 and childs[0][1] == level):
                    merkleTreeChild.append(childs[0][0])
                    childs.remove(childs[0])

            childs.append((MerkleTree(merkleTreeChild),level+1))
        return childs[0][0]
    
    def proofOfWork(self):
        pass

# n1 = Node()
# n1.transactions.append(Transaction('s','y','z'))
# n1.transactions.append(Transaction('g','h', 'o'))
# n1.transactions.append(Transaction('j','k','l'))
# n1.transactions.append(Transaction('y','l','z'))
# n1.transactions.append(Transaction('o','g','l'))


# n1.generateMerkleTree()



        
        
