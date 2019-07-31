#coding:utf-8

import sys
import json
import time
import pymysql
from flask import Flask, render_template, Blueprint, g, request, send_from_directory
from site_info_collect import runscan
from playsqlmap import start
import hashlib
app = Blueprint("trace", __name__)
'''
@app.before_request
def before_request():
    g.conn=pymysql.connect(user='root',host='localhost',database='autopentest')
    g.cur=g.conn.cursor()


@app.teardown_request
def tear_down(response):
    g.conn.close()
    return response
'''
@app.route("/trace", methods=['GET','POST'])
def trace():
	global target_urllist
	global iplist
	global collect_dirs
	global collect_ports
	global subdomain
	# try:
	result_infos = {}
	target = request.form["target"]  #获取网址
	target_urllist,iplist,collect_dirs,collect_ports,subdomain = runscan(target) #获取嗅探结果
	id = hashlib.md5()
	id.update(target.encode("utf8"))
	siteid = id.hexdigest()#将目标地址转化成唯一的哈希值
	try:
		for url in target_urllist[0:10:1]:
			start(siteid,url)
			time.sleep(0.3)
	except:
		print("在使用sqlmap时出错")
	print(target_urllist,iplist,collect_dirs,collect_ports,subdomain)
	# except:
	# 	print("这里出错了")
	return render_template("trace.html",target=target,target_urllist=target_urllist,iplist=iplist,collect_dirs=collect_dirs,collect_ports=collect_ports,subdomain=subdomain)
	# return render_template('trace.html',**locals())






