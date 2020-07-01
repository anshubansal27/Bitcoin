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
    txnFlag = True
    txnnodes = []
    # publicKeyMap = {hash --> id}
    publickeyMap = {}

    def __init__(self, id):
        # super(Node, self).__init__()
        self.id = id
        self.pubKey = []
        self.pvtKey = []
        self.blockchain = BlockChain()
        for i in range(5):
            key = RSA.generate(2048)
            self.pubKey.append(key.publickey().exportKey('PEM'))
            self.pvtKey.append(key.exportKey('PEM'))
            pubKeyHash = SHA256.new(hashlib.sha256(self.pubKey[i]).hexdigest().encode())
            Node.publickeyMap[pubKeyHash.hexdigest()] = str(self.id) +  " . " + str(i)

        self.transactions = []
        self.blockqueue = []
        self.target = None
        self.incentive = 0
        self.bitcoins = 0
        self.start = 0
        # self.utxo = {pubKeyHash: [(transactionHashPtr, transactionIndex), ... ] , .. }
        self.utxo = {}
        Transaction.keymap = Node.publickeyMap

    def getWalletAddress(self):
        keyno = randrange(0,5)
        pubKey = self.pubKey[keyno]
        keyhash = SHA256.new(hashlib.sha256(pubKey).hexdigest().encode())
        return keyhash

    def run(self):
        self.start = time.time()
        while(True):
            # print("in run")
            end = time.time()
            if(end - self.start > 10):
                if(len(self.transactions) > 0):
                    print("Creating block ")
                    blk = self.createBlock()
                    print(" #### creating block ####")
                    self.target = blk.hashVal
                    pow = self.proofOfWork()
                    if pow:
                        Node.txnFlag = False
                        print("In pow node id", self.id)

                        flag = True
                        for node in self.allNodes:
                            if node.getConsensus(blk) == False:
                                flag = False
                                break

                        if flag:
                            for node in self.allNodes:
                                node.processBlocks(blk)

                            for key in self.utxo:
                                # key, val = x[0], x[1]
                                val = self.utxo[key]
                                # print(val)
                                # print("key ", Node.publickeyMap[key])
                                # print("val ", val)
                                for y in val:
                                    print("Node id ", self.id ,"key ", Node.publickeyMap[key], "transaction amt ", y[0].output[y[1]][0])
                                # print("transaction amt", val[0].output[val[1]][0])
                                print("----------------------")
                            print(" # # # # # # # # # # # #")
                            Node.txnFlag = True
                            Node.txnnodes = []
                            self.incentive += incentive
                            randkeyno = randrange(0,5)
                            recverpubkeyHash = SHA256.new(hashlib.sha256(self.pubKey[randkeyno]).hexdigest().encode())
                            txn = Transaction([],[],incentive,recverpubkeyHash,None,True)
                            for node in self.allNodes:
                                node.processTransactions(txn)
                        else:
                            self.transactions = []
                            Node.txnFlag = True
                            Node.txnnodes = []
                    else:
                        self.start = time.time()
                    # self.transactions = []


            dotxn = random()

            if(dotxn <= 0.4 and Node.txnFlag and self.id not in Node.txnnodes):
                recvr = randrange(0,numberOfNodes)
                while(str(recvr) == str(self.id)):
                    recvr = randrange(0,numberOfNodes)
                recvrnode = self.allNodes[recvr]
                recvrkeyhash = recvrnode.getWalletAddress()
                prev_txn = []
                scriptsign = []
                # print("--- after script sign --")
                for j in range(5):
                    pkey = self.pubKey[j]
                    pvtkey = self.pvtKey[j]

                    try:
                        sendrpubkeyhash =  SHA256.new(hashlib.sha256(pkey).hexdigest().encode())
                        # print(sendrpubkeyhash.hexdigest())
                        txn_l = self.utxo[sendrpubkeyhash.hexdigest()]
                        for t in txn_l:
                            sendrPubKeyHash =  SHA256.new(hashlib.sha256(pkey).hexdigest().encode())
                            # print(" -- 1 --")
                            sendrPubKeyHash.update(t[0].hashVal.encode())
                            # print(" -- 2 --")
                            signer = PKCS115_SigScheme(RSA.importKey(pvtkey))
                            sendersignature = signer.sign(sendrPubKeyHash)
                            prev_txn.append(t)
                            scriptsign.append(ScriptSign(sendersignature, pkey))
                    except KeyError:
                        continue
                # bitcoinval = randrange(1,self.bitcoins+1)
                bitcoinval = randrange(10,51)
                print("#### 9")
                tempSender = sendrpubkeyhash.hexdigest()
                tempReceiver = recvrkeyhash.hexdigest()
                new_txn = Transaction(prev_txn,scriptsign,bitcoinval,recvrkeyhash,sendrpubkeyhash)
                print("#### 10")
                if new_txn.validTxn:
                    Node.txnnodes.append(self.id)
                    print("Sender ", Node.publickeyMap[tempSender], "Receiver ", Node.publickeyMap[tempReceiver])

                print("#### 11")
                for node in self.allNodes:
                    node.processTransactions(new_txn)

                print(" ##### 12")

                # self.bitcoins -= bitcoinval


            time.sleep(1)

    def getConsensus(self, block):
        if self.blockchain.latestBlock != block.prevBlockPtr:
            return False
        for txn in block.txnList:
            if txn.validTxn == False:
                return False
        return True

    def generateNonce(self):
        return randrange(0,2**sizeOfNonce)

    def processTransactions(self, txn):
        if(txn.validTxn):
            # print("valid txn")
            self.transactions.append(txn)
        # else:
        #     print("an invalid txn ..... ")

    def processBlocks(self,blck):
        # self.blockqueue.append(blck)
        if(self.blockchain.rootBlock == None):
            self.blockchain.rootBlock = blck

        self.blockchain.latestBlock = blck
        print("Block added to blockchain")

        print("block txn list len ", len(blck.txnList))

        # txnList = self.transactions.copy()
        # self.transactions = txnList
        temputxo = {}
        for txns in blck.txnList:
            for x in txns.input:
                index = x[0][1]
                scriptpubKey = x[0][0].output[index][1].recvrkeyHash
                try:
                    self.utxo[scriptpubKey] = []
                except KeyError:
                    continue
            index = 0
            for x in txns.output:
                scriptpubKey = x[1].recvrkeyHash
                try:
                    temputxo[scriptpubKey].append((txns,index))
                except KeyError:
                    temputxo[scriptpubKey] = [(txns, index)]
            # print("txn, index", txn, index)
                index += 1

            try:
                self.transactions.remove(txns)
            except ValueError:
                continue
        for key in temputxo:
            val = temputxo[key]
            for j in val:
                try:
                    self.utxo[key].append(j)
                except KeyError:
                    self.utxo[key] = [j]


        self.start = time.time()

    def createGenesisBlock(self):
        bitcoinvalue = 1000
        # txn = []
        # print(numberOfNodes//2)
        for _ in range(numberOfNodes):
            randomNo = randrange(0,numberOfNodes)
            randkeyno = randrange(0,5)
            node = self.allNodes[randomNo]
            recverpubkeyHash = SHA256.new(hashlib.sha256(node.pubKey[randkeyno]).hexdigest().encode())
            t1 = Transaction([],[],bitcoinvalue,recverpubkeyHash,None,True)
            self.transactions.append(t1)
        txn = self.transactions.copy()
        rootMerkleTree = self.generateMerkleTree(txn)
        blk = Block(None,rootMerkleTree,self.generateNonce(),txn)
        for node in self.allNodes:
            node.processBlocks(blk)

        self.transactions = []

        for key in self.utxo:
            # key, val = x[0], x[1]
            val = self.utxo[key]
            print("key ", Node.publickeyMap[key])
            # print("val ", val)
            for y in val:
                print("transaction amt ", y[0].output[y[1]][0])
            # print("transaction amt", val[0].output[val[1]][0])
            print("----------------------")
        print("----------------------  Genesis block ended  ---------------------")



    def createBlock(self):
        print("##### 14.1")
        txn = self.transactions.copy()
        rootMerkleTree = self.generateMerkleTree(txn)
        print("#### 14.2")
        blk = Block(self.blockchain.latestBlock,rootMerkleTree,self.generateNonce(),txn)
        print("#### 14.3")
        # self.transactions = []
        return blk


    def generateMerkleTree(self, txns):
        childs = []
        print("##### 15.1")
        for i in txns:
            childs.append((MerkleTree([i],True),0))
        print("##### 15.2")
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
    n1 = Node(i)
    nodesList.append(n1)
    n1.allNodes.append(n1)

nodesList[0].createGenesisBlock()
# nodesList[0].start()

with concurrent.futures.ThreadPoolExecutor(max_workers=numberOfNodes) as executor:
        for node in nodesList:
            executor.submit(run_thread,node)
