#!/usr/bin/python
#coding=utf-8
"""
*文件说明:urlmanager.py
*作者:高小调
*创建时间:2017年07月30日 星期日 20时36分38秒
*开发环境:Kali Linux/Python v2.7.13
"""
class UrlManager:
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    #添加一条新url
    def add_new_url(self,url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
    #添加很多url
    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
    #是否还有url
    def has_new_url(self):
        return len(self.new_urls)!=0
    #获取一条url
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url
