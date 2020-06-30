from BitcoinScripts import *
from config import *
from HashAlgo import *


class Transaction:
    keymap = {}

    def __init__(self, prev_txn, scriptSign, amnt, receiverPubKeyHash, senderPubKeyHash, genesisBlockTxn = False):
        # print("### 1")
        allHash = ""
        for txn in prev_txn:
            allHash += txn[0].hashVal + str(txn[1])

        # print("### 2")
        self.input = list(zip(prev_txn, scriptSign))
        self.validTxn = True
        self.output = []
        # self.out = [(value, scriptPubKEy), ]
        # print("before genesis block")
        # print("### 3")
        if(genesisBlockTxn):
            self.output.append((amnt, ScriptPubKey(receiverPubKeyHash)))
            for res in self.output:
                allHash += str(res[0]) + res[1].publicKeyHash.hexdigest()
            self.hashVal = generateHash(allHash)
            return

        # print("### 4")
        validCoins = self.isValidTxn(amnt)
        print("in validcoins Txn", validCoins)
        if validCoins == -1:
            self.hashVal = generateHash(allHash)
            self.validTxn = False
            return

        print("#### 4.1")

        self.output.append((amnt, ScriptPubKey(receiverPubKeyHash)))


        if validCoins > amnt:
           self.output.append( (validCoins - amnt, ScriptPubKey(senderPubKeyHash)) )

        # print("output size", len(self.output))
        for res in self.output:
            allHash += str(res[0]) + res[1].publicKeyHash.hexdigest()
        self.hashVal = generateHash(allHash)

        print("Sender from tran", Transaction.keymap[senderPubKeyHash.hexdigest()], "Receiver from trans ", Transaction.keymap[receiverPubKeyHash.hexdigest()], "amount ", amnt)
        # print("before rec pub key Hash")
        receiverPubKeyHash.update(self.hashVal.encode())
        senderPubKeyHash.update(self.hashVal.encode())
        # print("after rec pub key hash ")
        # print("after after after ")



    def isValidTxn(self, amnt):
        validBitCoins = 0
        for x in self.input:
            # print("### 5")
            index = x[0][1]
            scriptSign = x[1]
            scriptpubKey = x[0][0].output[index][1]
            # print("###### 5.1")
            if executeScripts(scriptSign, scriptpubKey) == False:
                # print("in executescript ")
                return -1
            validBitCoins += x[0][0].output[index][0]
            # print(" trans.py ",x[0][0].output[index][0])
            # print("### 6")
        # print("coins", validBitCoins)
        if validBitCoins < amnt:
            return -1
        # print("validCoin", validBitCoins)
        return validBitCoins


# senderkey = RSA.generate(2048)
# senderpubKey = senderkey.publickey().exportKey('PEM')
# senderpvtKey = senderkey.exportKey('PEM')

# sdrpubkeyhobj = SHA256.new(hashlib.sha256(senderpubKey).hexdigest().encode())
# sendrpubKeyhash = sdrpubkeyhobj.hexdigest()

# recvrkey = RSA.generate(2048)
# recvrpubKey = recvrkey.publickey().exportKey('PEM')
# recvrpvtKey = recvrkey.exportKey('PEM')
# recvrpubKeyHash = SHA256.new(hashlib.sha256(recvrpubKey).hexdigest().encode())


# txn = Transaction([],[],50,sdrpubkeyhobj,None,True)
# senderPrevTxn = [(txn , 0)]



# signer = PKCS115_SigScheme(RSA.importKey(senderpvtKey))
# sendersignature = signer.sign(sdrpubkeyhobj)


# txn1 = Transaction(senderPrevTxn,[ScriptSign(sendersignature,senderpubKey)], 50, recvrpubKeyHash, sdrpubkeyhobj)
