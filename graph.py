from config import *
from Node import *

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
