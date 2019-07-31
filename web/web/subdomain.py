import requests
from queue import Queue
from threading import Thread
import sys

header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
}
queue = Queue()
prefix_list = []
def getSub(url, prefix, subdomain):
    '''
    :param url: 网站子域名查询 api
    :param prefix: 子域名前缀 如 www email
    :param subdomain: 子域名 baidu.com
    :return: 输出存在的子域名
    '''
    url = url + prefix
    response = requests.get(url, headers=header).text

    status_code = response.split(',')[1].split(':')[1]
    if status_code == "200":
        prefix_list.append(prefix + "." + subdomain)
        print(prefix + "." + subdomain)

def thread(url, subdomain):
    '''
    :param url: 网站子域名查询 api
    :param subdomain: 子域名前缀 如 www email
    :return: 获取子域名，并调用子域名查询函数
    '''
    t = []
    while True:
        for i in range(1,100):
            prefix = queue.get()
            if queue.empty():
                break
            getSub(url, prefix.strip(), subdomain)

def getdic():
    '''
    :return: 读取字典
    '''
    with open('dict.txt', 'r', encoding='utf8') as f:
        while True:
            prefix = f.readline()
            if prefix == '':
                break
            queue.put(prefix)

def get_sub(domain):
    url = "https://phpinfo.me/domain/?domain=" + domain + "&q="
    thread1 = Thread(target=getdic)
    thread1.start()
    thread2 = Thread(target=thread, args=(url, domain))
    thread2.start()
    thread1.join()
    thread2.join()
    return prefix_list

print(get_sub('rongvideos.com'))