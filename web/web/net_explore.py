#!/usr/bin/env python
#coding = utf-8
# code by 92ez.com
# last modify time 2015-08-08 09:59
import queue
from threading import Thread
import time
import re
import os
import sys
import subprocess
import urllib.request
import urllib
os_char='gb18030'
#ip to num
def urlip(ip):
    apiurl = "http://www.gpsspg.com/ip/?q=%s" % ip
    content = urllib.request.urlopen(apiurl).read()
    reli = re.findall(u'<span class="fcg">(.*?)</span>',content)
    return reli

def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]


#num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,
                            (num & 0x00ff0000) >> 16,
                            (num & 0x0000ff00) >> 8,
                            num & 0x000000ff)
 
#get all ips list between start ip and end ip
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]
 
#main function
def bThread(iplist):
    global LOGFILE
    LOGFILE = open('netlog/TEMP.txt', 'w+')
    SETTHREAD = 800
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
        global PORT
        while not self.queuea.empty():
            host = self.queuea.get()
            try:
                #print host+":"+PORT1
                checkIP(host)
            except:
                continue
 
def checkIP(host):
    aimurl = "http://"+host+":80/"

 
    try:
        data = urllib.request.urlopen(aimurl,timeout = 5)
        htmlcontent = data.read()
        data.close()
 
        retitle = re.findall(u'<title>(.*?)</title>',htmlcontent)
        deip = urlip(host)
        #print "http://"+host+":"+PORT+"/" + " #"+retitle[0].decode("utf-8").encode(os_char)+"#"+deip[0].decode("utf-8").encode(os_char)
        try:

            LOGFILE.write("http://"+host +":"+PORT+"/"+" #"+retitle[0]+"#"+deip[0]+'\n')
        finally:
            LOGFILE.flush()
    except:
        pass

def netmain(addr):
    ipn = str(addr).split('.')
    ipcs = int(ipn[2]) - 1
    ipce = int(ipn[2]) + 1
    startip = ipn[0]+'.'+ipn[1]+'.'+str(ipcs)+'.'+'1'
    endip = ipn[0]+'.'+ipn[1]+'.'+str(ipce)+'.'+'255'

    iplist = ip_range(startip, endip)

    bThread(iplist)
