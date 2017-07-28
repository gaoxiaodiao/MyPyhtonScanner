#!/usr/bin/python
#coding=utf-8
"""
*文件说明:简单的端口扫描
*作者:高小调
*创建时间:2017年07月28日 星期五 14时01分38秒
*开发环境:Kali Linux/Python v2.7.13
"""
import socket
import threading
import Queue
import fcntl
import os
class PortScan:
    def __init__(self,ip="localhost",thread_num=10):
        self.PORT = {80:"web",8080:"web",3311:"kangle",3312:"kangle",3389:"mstsc",4440:"rundeck",5672:"rabbitMQ",5900:"vnc",6082:"varnish",7001:"weblogic",8161:"activeMQ",8649:"ganglia",9000:"fastcgi",9090:"ibm",9200:"elasticsearch",9300:"elasticsearch",9999:"amg",10050:"zabbix",11211:"memcache",27017:"mongodb",28017:"mondodb",3777:"dahua jiankong",50000:"sap netweaver",50060:"hadoop",50070:"hadoop",21:"ftp",22:"ssh",23:"telnet",25:"smtp",53:"dns",123:"ntp",161:"snmp",8161:"snmp",162:"snmp",389:"ldap",443:"ssl",512:"rlogin",513:"rlogin",873:"rsync",1433:"mssql",1080:"socks",1521:"oracle",1900:"bes",2049:"nfs",2601:"zebra",2604:"zebra",2082:"cpanle",2083:"cpanle",3128:"squid",3312:"squid",3306:"mysql",4899:"radmin",8834:'nessus',4848:'glashfish'}
        self.thread_num = thread_num    #线程数
        self.queue = Queue.Queue()      #被扫描端口队列
        self.ip = ip                    #被扫描ip
        #将待扫描端口入队
        for each_port in self.PORT.keys():
            self.queue.put(each_port)
    
    #端口扫描函数
    def _thread_scan(self):
        
        while not self.queue.empty():
            #取出一个端口
            port = self.queue.get()
            #创建套接字
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #设置超时时间
            sock.settimeout(1)
            try:
                #通过ip与端口号进行三次握手
                sock.connect((self.ip,port))
                #握手成功,表明该端口开放
                print "[port_scan]%s:%s OPEN [%s]"%(self.ip,port,self.PORT[port])
            except socket.error as msg:
                #被RST或者服务器无响应,表明该端口关闭
                print "[port_scan]%s:%s Close(%s)"%(self.ip,port,msg)
            finally:
                #最终关闭套接字
                sock.close()
    def run(self):
        '''
        threads=[]
        for i in range(self.thread_num):
            #创建线程
            t = threading.Thread(target=self._thread_scan())
            #将新线程放入列表中(方便回收)
            threads.append(t)
            #启动线程
            t.start()
        #回收线程
        for t in threads:
            t.join()
        '''
        self._thread_scan()
        print "[port_scan]The scan is complete!"
