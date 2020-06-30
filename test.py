import multiprocessing
import time


class Process(multiprocessing.Process):
    def __init__(self, id):
        super(Process, self).__init__()
        self.id = id

    def run(self):
        time.sleep(1)
        print("I'm the process with id: {}".format(self.id))


allprocess = []
for i in range(10):
    p = Process(i)
    allprocess.append(p)

for i in range(10):
    allprocess[i].start()
