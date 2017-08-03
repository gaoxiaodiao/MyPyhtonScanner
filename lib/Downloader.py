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
    def __init__(self):
        self.header = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    #get请求获取网页内容并返回
    def get(self,url):
        try:
            r = requests.get(url,timeout=10,headers=self.header)
            encoding = requests.utils.get_encodings_from_content(r.content)
            ret = r.content.decode(encoding[0]).encode('utf-8')
            return ret
        except Exception,e:
            print Exception,":",e
    #post请求获取网页内容并返回
    def post(self,url,data):
        try:
            r = requests.post(url,data)
            encoding = requests.utils.get_encodings_from_content(r.content)
            ret = r.content.decode(encoding[0]).encode('utf-8')
            return ret
        except Exception,e:
            print Exception,":",e
    #将页面down下来,放到htmls中
    def down(self,url,htmls):
        if url is None:
            return None;
        strs = {}
        strs["url"] = url
        try:
            r = requests.get(url,timeout=10)
            encoding = requests.utils.get_encodings_from_content(r.content)
            ret = r.content.decode(encoding[0]).encode('utf-8')
            if r.status_code != 200:
                return ret
            strs["html"] = ret
        except Exception,e:
            print Exception,":",e
        htmls.append(strs)
