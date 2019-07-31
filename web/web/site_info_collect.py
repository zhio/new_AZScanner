import re
import requests
from bs4 import BeautifulSoup
from save_to_mysql import addurls
from dirfuzz import fuzz_start
from site_port_check import portScan
from scaner import ScanPort
urllist =[]
iplist =[]

def get(target_url):
    try:
        i_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'
        }
        response = requests.get(target_url,headers=i_headers)
        body_text = response.text
    except:
        print('获取网页失败')
    return body_text

def get_url(body_text):
        soup=BeautifulSoup(body_text,'lxml')
        links=soup.findAll('a')
        for link in links:
            url =link.get('href')
            try:
                if '?' in str(url):
                    urllist.append(url)

            except:
                pass

#获取ip地址列表
def get_ip(body_text):
    body_text=body_text.replace(" ","")
    ips=re.findall(r"\d+\.\d+\.\d+\.\d+",body_text,re.I)
    for i in ips:
        iplist.append(i)

def subdomainapi2(target_url):
    if 'www' in target_url:
        try:
            target_url = target_url.strip('http:').strip('/').strip('www.')
            headers = {
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
            }
            res = requests.get('http://site.ip138.com/{}/domain.htm'.format(target_url), headers=headers)
            p = re.compile(r'target="_blank">(.*?)</a></p>')
            sub = p.findall(res.text)
            # print(res.text)
            if (len(sub) == 0):
                print('[+] ip138接口可能出现问题!')
            return sub
        except:
            pass
    else:
        return None
def runscan(target_url):
    global urllist
    global iplist
    urllist = []
    iplist = []
    list1 = []
    list2 = []

    body_text = get(target_url)
    get_ip(body_text)

    get_url(body_text)
    iplist = list(set(iplist))
    for i in urllist:
        if 'http://' not in i:
            i = target_url + i
            list1.append(i)
        else:
            list2.append(i)
    target_urllist = list(set(list1).union(set(list2)))
    collect_dirs = fuzz_start(target_url)
    collect_dirs= list(set(collect_dirs))
    collect_dirs = collect_dirs[:100]
    collect_ports = ScanPort(target_url).pool()
    subdomain = subdomainapi2(target_url)#子域名
    addurls(str(target_url),str(target_urllist),str(iplist),str(collect_dirs),str(collect_ports),str(subdomain))
    return target_urllist,iplist,collect_dirs,collect_ports,subdomain
