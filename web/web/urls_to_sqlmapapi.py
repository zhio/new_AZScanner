__author__ = 'AZONE'
import urllib
import urllib.request
import json
import requests
def run_server():
    pass
    #os.system("python H:\zoomeye_spider\auto-pentest\sqlmap\sqlmapapi.py -s -p 8080")
def creat_task():
    try:
        url = 'http://127.0.0.1:8080/task/new'
        response = urllib.request.urlopen(url)
        jdata = json.loads(response.read())
        taskid = str(jdata['taskid'])
    except:
        pass
    return taskid
'''
class task():
    def __int__(self,target_url):
        self.taskid = creat_task()
        self.url = target_url
    def get_status(self):
        url='http://127.0.0.1:8080/scan/'+self.taskid+'/status'
        response = urllib2.urlopen(url)
        print response.read()
    def get_log(self):
        url='http://127.0.0.1:8080/scan/'+self.taskid+'/log'
        response = urllib2.urlopen(url)
        print response.read()
    def get_data(self):
        url='http://127.0.0.1:8080/scan/'+self.taskid+'/data'
        response = urllib2.urlopen(url)
        print response.read()
    def task_start(self):
        url='http://127.0.0.1:8080/scan/'+self.taskid+'/start'
        value ={'url':self.url}
        i_headers = {'Content-Type':'application/json'}
        jdata = json.dumps(value)
        req = urllib2.Request(url, jdata,headers=i_headers)
        response = urllib2.urlopen(req)
        print response.read()
ret = #creat_task()
'''
def viewtask(taskid):
        url='http://127.0.0.1:8080/scan/'+taskid+'/log'
        response = urllib.request.urlopen(url)
        return response.read()
def viewdata(taskid):
        url='http://127.0.0.1:8080/scan/'+taskid+'/data'
        response = urllib.request.urlopen(url)
        return response.read()
def task_start(taskid,url):

    url='http://127.0.0.1:8080/scan/'+taskid+'/start'
    value ={'url':url}
    i_headers = {'Content-Type':'application/json'}
    jdata = json.dumps(value)
    # req = urllib.request.Request(url, data=bytes(urllib.parse.urlencode(jdata),'UTF8'),headers=i_headers)
    req = requests.post(url,data=jdata,headers = i_headers)
    print(req.text)
    return req.text
    # response = urllib.request.urlopen(req)
    # return response.read()
def get_status(taskid):
        url='http://127.0.0.1:8080/scan/'+taskid+'/status'
        response = urllib.request.urlopen(url)
        return response.read()
# print (task_start(taskid,'http://www.biditcapital.com/SmallScale/Detial?id=7ab81122-0356-4942-a7ee-169b2afdfa4f'))




