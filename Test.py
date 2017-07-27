#!/usr/bin/python
#coding=utf-8
"""
*文件说明:测试各种函数
*作者:高小调
*创建时间:2017年07月27日 星期四 16时15分18秒
*开发环境:Kali Linux/Python v2.7.13
"""
from modules import cdn_check
def test_get_domain():
    print cdn_check.get_domain("http://blog.csdn.net/imzoer/article/details/8636764")
    print cdn_check.get_domain("http://www.cnblogs.com/allenblogs/archive/2011/11/15/2055149.html")
    print cdn_check.get_domain("https://my.oschina.net/guol/blog/95699")
    print cdn_check.get_domain("")

if __name__ == '__main__':
    test_get_domain()
