#coding:utf-8
import os
import importlib
import sys
from flask import Flask, render_template, Blueprint, g, request
import json
import pymysql
from playsqlmap import get_status,viewdata,viewtask
from save_to_mysql import adtasklog
import socket
from net_explore import netmain
app = Blueprint("address_manager", __name__)

@app.route("/manager", methods = ["GET",'POST']) #任务列表
def get_info():
    conn=pymysql.connect(user='root',host='localhost',database='autopentest')
    cur=conn.cursor()
    sql = "select id,url from target_baseinfo"
    cur.execute(sql)
    result_infos = cur.fetchall()
    cur.close()
    return render_template("manager.html", result_infos = result_infos)


@app.route("/view/<id>", methods=["GET",'POST'])
def view(id):
    conn=pymysql.connect(user='root',host='localhost',database='autopentest')
    cur=conn.cursor()
    sql = "select * from target_baseinfo where id = '{}'".format(id)
    cur.execute(sql)
    result_infos = cur.fetchone()
    result_infos = result_infos
    cur.close()
    return render_template("view.html",result_infos = result_infos)

@app.route("/checksqli/<id>", methods=["GET",'POST'])
def checksqli(id):
    conn=pymysql.connect(user='root',host='localhost',database='autopentest')
    cur=conn.cursor()
    sql = "select * from sqlmaptask where siteid = '{}'".format(id)
    cur.execute(sql)
    result_infos = cur.fetchall()
    return render_template("checksqli.html",result_infos = result_infos)
    cur.close()
@app.route("/getlog/<id>", methods=["GET",'POST'])
def getlog(id):

    conn=pymysql.connect(user='root',host='localhost',database='autopentest')
    cur=conn.cursor()
    sql = "select * from sqlmaptask_info where taskid = '{}'".format(id)
    cur.execute(sql)
    result_infos = cur.fetchone()
    if result_infos:
        id = result_infos[0]
        log = result_infos[1]
        data = result_infos[2]


    else:
        ret = get_status(id)
        jdata = json.loads(ret)
        status = str(jdata['status'])
        if status == 'terminated':
            log = viewtask(id)
            data = viewdata(id)
            adtasklog(id,log,data)
    return render_template("getlog.html",id=id,log = log,data=data)
    cur.close()

@app.route("/netexplore/<id>", methods=["GET",'POST'])
def netexplore(id):
    url = id
    try:
        addr = socket.getaddrinfo(url,'http')[0][4][0]
        netmain(addr)
        f = open('netlog/'+addr+'.txt','r')
        alllines=f.readlines()
        f.close()
    except:
        pass
    return render_template("netlist.html")

'''
@app.route("/inject/<id>", methods=["GET",'POST'])
def view(id):
    conn=mysql.connector.connect(user='root',password='pass',host='localhost',database='autopentest')
    cur=conn.cursor()
    sql = "select collect_urls from target_baseinfo where id = '{}'".format(id)
    cur.execute(sql)
    result_infos = cur.fetchone()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    cur.close()
'''

