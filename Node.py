from random import randrange
from config import *
from Crypto.PublicKey import RSA
from MerkleTree import MerkleTree
from Transaction import *
from Blockchain import *
from Block import *
import multiprocessing
import time
from random import random


class Node(multiprocessing.Process):
    allNodes = []

    def __init__(self):
        self.pubKey = []
        self.pvtKey = []
        self.blockchain = BlockChain()
        for i in range(5):
            key = RSA.generate(2048)
            self.pubKey.append(key.publickey().exportKey('PEM'))
            self.pvtKey.append(key.exportKey('PEM'))
        self.transactions = []
        self.blockqueue = []
        self.target = None
        self.incentive = 0
        self.bitcoins = 0
        # self.utxo = {pubKeyHash: [(transactionHashPtr, transactionIndex), ... ] , .. }
        self.utxo = {}

    def getWalletAddress(self):
        keyno = randrange(0,5)
        pubKey = self.pubKey[keyno]
        keyhash = SHA256.new(hashlib.sha256(pubKey).hexdigest().encode())
        return keyhash

    def run(self):
        start = time.time()
        while(True):
            end = time.time()
            if(end - time > 60):
                start = time.time()
                blk = self.createBlock()
                self.target = blk.hashVal
                pow = self.proofOfWork()
                if pow:
                    for node in self.allNodes:
                        node.processBlocks(blk)
                    self.transactions = []
            
            dotxn = random()

            if(dotxn <= 0.5 and self.bitcoins > 0):
                recvr = randrange(0,numberOfNodes)
                recvrnode = self.allNodes[recvr]
                recvrkeyhash = recvrnode.getWalletAddress()
                prev_txn = []
                scriptsign = []
                for j in range(5):
                    pkey = self.pubKey[j]
                    pvtkey = self.pvtKey[j]
                    sendrpubkeyhash =  SHA256.new(hashlib.sha256(pkey).hexdigest().encode()) 
                    signer = PKCS115_SigScheme(RSA.importKey(senderpvtKey))
                    sendersignature = signer.sign(sendrpubkeyhash)
                    try:
                        txn_l = self.utxo[sendrpubkeyhash.hexdigest()]
                        for t in txn_l:
                            prev_txn.append(t)
                            scriptsign.append(sendersignature)
                    except KeyError:
                        continue
                bitcoinval = randrange(1,self.bitcoins+1)
                new_txn = Transaction(prev_txn,scriptSign,bitcoinval,recvrkeyhash,sendrpubkeyhash)
                for node in self.allNodes:
                    node.processTransactions(new_txn)
                self.bitcoins -= bitcoinval


            time.sleep(1)

    def generateNonce(self):
        return randrange(0,2**sizeOfNonce)

    def processTransactions(self, txn):
        if(txn.validTxn):
            self.transactions.append(txn)
        else:
            print("an invalid txn ..... ")

    def processBlocks(self,blck):
        # self.blockqueue.append(blck)
        if(self.blockchain.rootBlock == None):
            self.blockchain.rootBlock = blck
        self.blockchain.latestBlock = blck
        for txns in blck.txnList:
            for x in txns.input:
                index = x[0][1]
                scriptpubKey = x[0][0].output[index][1]
                try:
                    self.utxo[scriptpubKey.hexdigest()] = []
                except KeyError:
                    continue
            index = 0
            for x in txns.output:
                scriptpubKey = x[1].publicKeyHash
                self.utxo[scriptpubKey.hexdigest()].append((txns,index))
                index += 1 
            
    def createGenesisBlock(self):
        bitcoinvalue = 50
        # txn = []
        for i in range(numberOfNodes/2):
            randomNo = randrange(0,numberOfNodes)
            randkeyno = randrange(0,5)
            node = self.allNodes[randomNo]
            recverpubkeyHash = SHA256.new(hashlib.sha256(node.pubKey[randkeyno]).hexdigest().encode())
            t1 = Transaction([],[],bitcoinvalue,recverpubkeyHash,None,True)
            self.transactions.append(t1)
        rootMerkleTree = self.generateMerkleTree()
        blk = Block(None,rootMerkleTree,self.generateNonce(),self.transactions)
        for node in self.allNodes:
            node.processBlocks(blk)
        
        self.transactions = []


    def createBlock(self):
        rootMerkleTree = self.generateMerkleTree()
        blk = Block(self.blockchain.latestBlock,rootMerkleTree,self.generateNonce(),self.transactions)
        # self.transactions = []
        return blk


    def generateMerkleTree(self):
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
        for node in self.allNodes:
            if(self.target > node.target):
                return False
        return True

# n1 = Node()
# n1.transactions.append(Transaction('s','y','z'))
# n1.transactions.append(Transaction('g','h', 'o'))
# n1.transactions.append(Transaction('j','k','l'))
# n1.transactions.append(Transaction('y','l','z'))
# n1.transactions.append(Transaction('o','g','l'))


# n1.generateMerkleTree()
nodesList = []
for i in range(numberOfNodes):
    n1 = Node()
    nodesList.append(n1)
    Node.allNodes.append(n1)





