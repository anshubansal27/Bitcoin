from config import *
from Transaction import *
from HashAlgo import *
class MerkleTree:
    def __init__(self, child, txnflag = False):
        if(txnflag):
            self.hashvalue = "xy"
            print("txn")
        else:
            allHashVal = ""
            for i in child:
                allHashVal += i.hashvalue
            print(allHashVal)
            self.hashvalue = allHashVal
            # self.hashvalue = generateHash(allHashVal)
            
        self.childs = child
        self.txn = txnflag


# t1 = Transaction('x','y','z')
# t2 = Transaction('y','z','t')

# m1 = MerkleTree([t1], "A", True)
# m2 = MerkleTree([t2],"B", True)

# m3 = MerkleTree([m1,m2],"C")

# t3 = Transaction('x','y','z')
# t4 = Transaction('y','z','t')

# m4 = MerkleTree([t3],"D", True)
# m5 = MerkleTree([t4],"E", True)

# m6 = MerkleTree([m4,m5],"F")

# m7 = MerkleTree([m3,m6],"G")








