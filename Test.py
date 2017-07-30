#!/usr/bin/python
#coding=utf-8
"""
*文件说明:测试各种函数
*作者:高小调
*创建时间:2017年07月27日 星期四 16时15分18秒
*开发环境:Kali Linux/Python v2.7.13
"""
from modules import cdn_check
from modules import port_scan
import requests
from sys import argv
from lib import Spider

#测试从url中获取域名
def test_get_domain():
    print cdn_check.get_domain("http://blog.csdn.net/imzoer/article/details/8636764")
    print cdn_check.get_domain("http://www.cnblogs.com/allenblogs/archive/2011/11/15/2055149.html")
    print cdn_check.get_domain("https://my.oschina.net/guol/blog/95699")
    print cdn_check.get_domain("")

#测试表单数据
def test_get_post_request_info():
    url = "http://ce.cloud.360.cn"
    web_content = requests.get(url)
    print cdn_check.get_post_request_info(web_content.text)

#测试cdn检测
def test_cdn_check():
    script,first = argv
    msg,state=cdn_check.run(first)
    print msg

#测试端口扫描
def test_port_scan():
    script,ip = argv
    if ip == None:
        print "Usage:%s [ip]"%script
        return False
    ps = port_scan.PortScan(ip)
    ps.run()

#测试小爬虫
def test_spider():
    s = Spider.Spider("http://blog.gaoxiaodiao.com",10);
    s.craw()
if __name__ == '__main__':
    #test_get_domain()
    #test_get_post_request_info()
    #test_cdn_check()
    #test_port_scan()
    test_spider()
