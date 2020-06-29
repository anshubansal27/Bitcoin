from BitcoinScripts import *
from config import *
from HashAlgo import *


class Transaction:
    def __init__(self, prev_txn, scriptSign, amnt, receiverPubKeyHash, senderPubKeyHash):

        allHash = ""
        for txn in prev_txn:
            allHash += txn[0].hashVal + str(txn[1])

        self.input = list(zip(prev_txn, scriptSign))
        self.validTxn = True
        self.output = []
        # self.out = [(value, scriptPubKEy), ]

        validCoins = self.isValidTxn(amnt)
        if validCoins == -1:
            self.hashVal = generateHash(allHash)
            self.validTxn = False
            return


        self.output.append((amnt, ScriptPubKey(receiverPubKeyHash)))

        if validCoins > amnt:
           self.output.append( (validCoins - amnt, ScriptPubKey(senderPubKeyHash)) )

        for res in self.output:
            allHash += str(res[0]) + res[1].publicKeyHash
        self.hashVal = generateHash(allHash)



    def isValidTxn(self, amnt):
        validBitCoins = 0
        for x in self.input:
            index = x[0][1]
            scriptSign = x[1]
            scriptpubKey = x[0][0].output[index][1]
            if executeScripts(scriptSign, scriptpubKey) == False:
                return -1
            validBitCoins += x[0][0].output[index][0]
        if validBitCoins < amnt:
            return -1
        return validBitCoins
