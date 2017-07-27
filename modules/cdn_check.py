#!/usr/bin/python
#coding=utf-8
"""
*文件说明:检测网站是否存在CDN/云WAF(多节点)
*作者:高小调
*创建时间:2017年07月27日 星期四 15时39分27秒
*开发环境:Kali Linux/Python v2.7.13
*参考于某个大神的github:https://github.com/Xyntax/POC-T/blob/2.0/script/cdn-detect.py
*结果(未使用):
*http://forexample.com Nodes:XX IP(1):XXX:XXX:XXX:XXX
*结果(使用):
*http://forexample.com [CDN FOUND!] Node:XX IP:XXX:XXX:XXX:XXX1 XXX:XXX:XXX:XXX2 ....
*结果(其他情况):
*http://forexample.com [Target Unknown]
"""
import requests                     #url请求
import re                           #正则表达式
import time                         #日期时间库
from bs4 import BeautifulSoup       #html解析库
import urlparse                     #url解析

'''
从url中获取其域名
Use:
http://forexample.com/index.asp?id=xxx&cate=xxx
Return:
http://forexample.com
'''
def get_domain(url):
    #(sheme='http',netloc='forexample',path='/index.asp',params='',query='id=xxx&cate=xxx',fargment='')
    tmp = urlparse.urlparse(url)                                    #解析url
    return urlparse.urlunsplit([tmp.scheme,tmp.netloc,'','',''])    #拼接url
