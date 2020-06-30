import concurrent.futures
import multiprocessing
import threading
import time
from random import random, randrange

from Crypto.PublicKey import RSA

from Block import *
from Blockchain import *
from config import *
from MerkleTree import MerkleTree
from Transaction import *


class Node:
    allNodes = []

    def __init__(self):
        # super(Node, self).__init__()
        self.pubKey = []
        self.pvtKey = []
        self.blockchain = BlockChain()
        for _ in range(5):
            key = RSA.generate(2048)
            self.pubKey.append(key.publickey().exportKey('PEM'))
            self.pvtKey.append(key.exportKey('PEM'))
        self.transactions = []
        self.blockqueue = []
        self.target = None
        self.incentive = 0
        self.bitcoins = 0
        self.start = 0
        # self.utxo = {pubKeyHash: [(transactionHashPtr, transactionIndex), ... ] , .. }
        self.utxo = {}

    def getWalletAddress(self):
        keyno = randrange(0,5)
        pubKey = self.pubKey[keyno]
        keyhash = SHA256.new(hashlib.sha256(pubKey).hexdigest().encode())
        return keyhash

    def run(self):
        self.start = time.time()
        while(True):
            print("in run")
            end = time.time()
            if(end - self.start > 60):
                print("Creating block ")
                blk = self.createBlock()
                self.target = blk.hashVal
                pow = self.proofOfWork()
                if pow:
                    print("In pow ")
                    for node in self.allNodes:
                        node.processBlocks(blk)
                    for key in self.utxo:
                        # key, val = x[0], x[1]
                        val = self.utxo[key]
                        print("key ", key)
                        # print("val ", val)
                        for y in val:
                            print("transaction amt ", y[0].output[y[1]][0])
                        # print("transaction amt", val[0].output[val[1]][0])
                        print("----------------------")
                    # self.transactions = []


            dotxn = random()

            if(dotxn <= 0.5 ):
                recvr = randrange(0,numberOfNodes)
                recvrnode = self.allNodes[recvr]
                recvrkeyhash = recvrnode.getWalletAddress()
                prev_txn = []
                scriptsign = []
                print("--- after script sign --")
                for j in range(5):
                    pkey = self.pubKey[j]
                    pvtkey = self.pvtKey[j]
                    sendrpubkeyhash =  SHA256.new(hashlib.sha256(pkey).hexdigest().encode())
                    signer = PKCS115_SigScheme(RSA.importKey(pvtkey))
                    sendersignature = signer.sign(sendrpubkeyhash)
                    try:
                        print(sendrpubkeyhash.hexdigest())
                        txn_l = self.utxo[sendrpubkeyhash.hexdigest()]
                        for t in txn_l:
                            prev_txn.append(t)
                            scriptsign.append(sendersignature)
                    except KeyError:
                        continue
                # bitcoinval = randrange(1,self.bitcoins+1)
                bitcoinval = 5
                print("prev trans len ", len(prev_txn))
                new_txn = Transaction(prev_txn,scriptsign,bitcoinval,recvrkeyhash,sendrpubkeyhash)
                for node in self.allNodes:
                    node.processTransactions(new_txn)
                # self.bitcoins -= bitcoinval


            # time.sleep(1)

    def generateNonce(self):
        return randrange(0,2**sizeOfNonce)

    def processTransactions(self, txn):
        if(txn.validTxn):
            print("valid txn")
            self.transactions.append(txn)
        # else:
        #     print("an invalid txn ..... ")

    def processBlocks(self,blck):
        # self.blockqueue.append(blck)
        if(self.blockchain.rootBlock == None):
            self.blockchain.rootBlock = blck
        self.blockchain.latestBlock = blck

        txnList = self.transactions.copy()
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
                try:
                    self.utxo[scriptpubKey.hexdigest()].append((txns,index))
                except KeyError:
                    self.utxo[scriptpubKey.hexdigest()] = [(txns, index)]
            # print("txn, index", txn, index)
                index += 1

            try:
                txnList.remove(txns)
            except ValueError:
                continue

        self.transactions = txnList

        self.start = time.time()

    def createGenesisBlock(self):
        bitcoinvalue = 50
        # txn = []
        # print(numberOfNodes//2)
        for _ in range(numberOfNodes):
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

        for key in self.utxo:
            # key, val = x[0], x[1]
            val = self.utxo[key]
            print("key ", key)
            # print("val ", val)
            for y in val:
                print("transaction amt ", y[0].output[y[1]][0])
            # print("transaction amt", val[0].output[val[1]][0])
            print("----------------------")
        print("----------------------  Genesis block ended  ---------------------")



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
            if(node.target is not None and self.target > node.target):
                return False
        return True

# n1 = Node()
# n1.transactions.append(Transaction('s','y','z'))
# n1.transactions.append(Transaction('g','h', 'o'))
# n1.transactions.append(Transaction('j','k','l'))
# n1.transactions.append(Transaction('y','l','z'))
# n1.transactions.append(Transaction('o','g','l'))


# n1.generateMerkleTree()

def run_thread(node):
    # print("in run thread")
    node.run()


nodesList = []
for i in range(numberOfNodes):
    n1 = Node()
    nodesList.append(n1)
    n1.allNodes.append(n1)

nodesList[0].createGenesisBlock()
# nodesList[0].start()

with concurrent.futures.ThreadPoolExecutor(max_workers=numberOfNodes) as executor:
        for node in nodesList:
            executor.submit(run_thread,node)
