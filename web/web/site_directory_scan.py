__author__ = 'AZONE'
import queue
from threading import Thread
import sys
import urllib

def bThread(iplist):
    SETTHREAD = 800
    print ('[Note] Running...\n')
    threadl = []
    queuea = queue.Queue()
    hosts = iplist
    for host in hosts:
        queuea.put(host)

    threadl = [tThread(queuea) for x in range(0, int(SETTHREAD))]
    for t in threadl:
        t.start()
    for t in threadl:
        t.join()

#create thread
class tThread(Thread):

    def __init__(self, queuea):
        Thread.__init__(self)
        self.queuea = queuea

    def run(self):
        while not self.queuea.empty():
            host = self.queuea.get()
            try:
                Dirbruteforce(host)
            except:
                continue
def Dirbruteforce(mydir):
    target_url = 'http://jf.cmbchina.com/'
    status=urllib.urlopen(target_url+mydir).code
    #if status == '200':
    print (target_url+mydir +"###:"+status)
dicdir = []
fp=open("dic/asp.list", "r")
alllines=fp.readlines()
for eachline in alllines:
        eachline=eachline.strip('\n')
        dicdir.append(eachline)
bThread(dicdir)