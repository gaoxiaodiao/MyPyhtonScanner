#!/usr/bin/python
#coding=utf-8
"""
*文件说明:爬虫的下载器
*作者:高小调
*创建时间:2017年07月30日 星期日 20时27分52秒
*开发环境:Kali Linux/Python v2.7.13
"""
import requests
class Downloader:
    #get请求获取网页内容并返回
    def get(self,url):
        r = requests.get(url,timeout=10)
        if r.status_code != 200:
            return None;
        content = r.text
        return content
    #post请求获取网页内容并返回
    def post(self,url,data):
        r = requests.post(url,data)
        content = r.text;
        return content
    #将页面down下来,放到htmls中
    def down(self,url,htmls):
        if url is None:
            return None;
        strs = {}
        strs["url"] = url
        try:
            r = requests.get(url,timeout=10)
            if r.status_code != 200:
                return None
            strs["html"] = r.text
        except Exception,e:
            print Exception,":",e
        htmls.append(strs)
