#!/usr/bin/python
#coding=utf-8
"""
*文件说明:spider.py
*作者:高小调
*创建时间:2017年07月30日 星期日 20时27分14秒
*开发环境:Kali Linux/Python v2.7.13
"""
import Downloader,UrlManager
import threading
from urlparse import urljoin
from bs4 import BeautifulSoup
class Spider:
    def __init__(self,root,thread_num):
        self.urls = UrlManager.UrlManager()
        self.downloader = Downloader.Downloader()
        self.root = root
        self.thread_num = thread_num
    
    #判断url是否属于domain
    def _judge(self,domain,url):
        if (url.find(domain) != -1):
            return True
        else:
            return False

    #从当前url中获取新的urls
    def _get_new_urls(self,page_url,content):
        if content is None:
            return
        soup = BeautifulSoup(content,"html.parser")

        new_urls = set()
        links = soup.find_all('a')
        for link in links:
            new_url = link.get("href")
            new_full_url = urljoin(page_url,new_url)
            if(self._judge(self.root,new_full_url)):
                new_urls.add(new_full_url)
        return new_urls

    #爬取
    def craw(self):
        self.urls.add_new_url(self.root)
        #只要url管理器中还存在新url,则不断的爬取
        while self.urls.has_new_url():
            contents = []
            threads = []
            for i in list(range(self.thread_num)):
                if self.urls.has_new_url() is False:
                    #url管理器中没有新url,则跳出循环
                    break;
            new_url = self.urls.get_new_url()
            print "[Spider]",new_url
            t = threading.Thread(target=self.downloader.down,args=(new_url,contents))
            t.start()
            threads.append(t)
            for thread in threads:
                thread.join()

            for _str in contents:
                if _str is None:
                    continue
                new_urls = self._get_new_urls(new_url,_str['html'])
                self.urls.add_new_urls(new_urls)
