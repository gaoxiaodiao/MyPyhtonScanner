#!/usr/bin/python
#coding=utf-8
"""
*文件说明:检测网站是否存在CDN/云WAF(多节点)
*作者:高小调
*创建时间:2017年07月27日 星期四 15时39分27秒
*开发环境:Kali Linux/Python v2.7.13
*
*本代码参考于:https://github.com/Xyntax/POC-T/blob/2.0/script/cdn-detect.py
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

#获取http://ce.cloud.360.cn/表单的信息,目的是构造Post请求参数
def get_post_request_info(web_content):
    _ret_dict = {}
    soup = BeautifulSoup(web_content,"html.parser")
    for each_input_elem in soup.find_all('input'):
        if 'name' in each_input_elem.attrs and 'value' in each_input_elem.attrs: 
            #print each_input_elem['name'] + ":"+ each_input_elem['value']
            _ret_dict[each_input_elem['name']] = each_input_elem['value']
    return _ret_dict

#检测CDN核心代码
def run(url):
    domain = get_domain(url)
    dest = "http://ce.cloud.360.cn"
    error_msg = domain + "[Target Unknow]"
    #构建请求数据
    s = requests.session()
    request_info = get_post_request_info(s.get(dest).content)
    request_info['domain'] = domain
    #对task进行post请求
    post_ret = s.post("http://ce.cloud.360.cn/task",data=request_info)
    if(post_ret.status_code!=200):
        print "[cdn_detector]:task post failure,status code is " + str(post_ret.status_code)
        return error_msg,False
    else:
        print "[cdn_detector]:task post successful!"
    request_header = {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    #对detect进行post请求
    post_ret = s.post("http://ce.cloud.360.cn/Tasks/detect",data=request_info,headers=request_header)
    if(post_ret.status_code != 200):
        print "[cdn_detector]:detect post failure,status code is " + str(post_ret.statuc_code)
        return error_msg,False
    else:
        print "[cdn_detector]:detect post successful"
    #延时6秒,为了让远端主机有尽可能多的时间去探测目的主机
    time.sleep(6)
    request_info2 = 'domain=' + domain + '&type=get&ids%5B%5D=1&ids%5B%5D=2&ids%5B%5D=3&ids%5B%5D=4&ids%5B%5D=5&ids%5B%5D=6&ids%5B%5D=7&ids%5B%5D=8&ids%5B%5D=9&ids%5B%5D=16&ids%5B%5D=18&ids%5B%5D=22&ids%5B%5D=23&ids%5B%5D=41&ids%5B%5D=45&ids%5B%5D=46&ids%5B%5D=47&ids%5B%5D=49&ids%5B%5D=50&ids%5B%5D=54&ids%5B%5D=57&ids%5B%5D=58&ids%5B%5D=61&ids%5B%5D=62&ids%5B%5D=64&ids%5B%5D=71&ids%5B%5D=78&ids%5B%5D=79&ids%5B%5D=80&ids%5B%5D=93&ids%5B%5D=99&ids%5B%5D=100&ids%5B%5D=101&ids%5B%5D=103&ids%5B%5D=104&ids%5B%5D=106&ids%5B%5D=110&ids%5B%5D=112&ids%5B%5D=114&ids%5B%5D=116&ids%5B%5D=117&ids%5B%5D=118&ids%5B%5D=119&ids%5B%5D=120&ids%5B%5D=121&ids%5B%5D=122&user_ip_list='
    post_ret = s.post('http://ce.cloud.360.cn/GetData/getTaskDatas', data=request_info2, headers=request_header)
    #如果本次请求失败,则尝试三次,直到成功为止.
    try_time = 0;
    while(post_ret.status_code!=200 and try_time < 3):
        print "[cdn_detector]get info failure,status code is " + str(post_ret.status_code) + ",try again"
        try_time += 1
    #三次请求都未成功,探测失败
    if(post_ret.status_code!=200):
        print "[cdn_detector]try three times already,i am angry,bye!"
        return error_msg,False
    #从响应的数据中提取ip
    ips = re.findall('"ip":"(.*?)"',post_ret.content)
    ans = list(set(ips))
    
    if not len(ips):
        return error_msg,False
    success_msg = url;
    success_msg += '[CDN FOUND!]' if len(ans) > 1 else ''
    success_msg += 'Nodes:' + str(len(ips))
    success_msg += 'Ip(%s)' % str(len(ans)) + ' '.join(ans)
    return success_msg,True
