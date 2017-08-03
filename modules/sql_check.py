#!/usr/bin/python
#coding=utf-8
"""
*文件说明:简单的判断页面是否存在sql注入漏洞
*作者:高小调
*创建时间:2017年07月31日 星期一 15时17分22秒
*开发环境:Kali Linux/Python v2.7.13
"""
import sys
import re
import random
sys.path.append("..")
from lib import Downloader
def run(url):
    if not url.find("/"):
        return False
    downloader = Downloader.Downloader()
    BOOLEAN_TESTS = (" And %d=%d"," OR ONT %d=%d")
    DBMS_ERRORS = {# regular expressions used for DBMS recognition based on error message response
        "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
        "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\."),
        "Microsoft SQL Server": (r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*mssql_.*", r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}", r"(?s)Exception.*\WSystem\.Data\.SqlClient\.", r"(?s)Exception.*\WRoadhouse\.Cms\."),
        "Microsoft Access": (r"Microsoft Access Driver", r"JET Database Engine", r"Access Database Engine"),
        "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*"),
        "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error", r"\bdb2_\w+\("),
        "SQLite": (r"SQLite/JDBCDriver", r"SQLite.Exception", r"System.Data.SQLite.SQLiteException", r"Warning.*sqlite_.*", r"Warning.*SQLite3::", r"\[SQLITE_ERROR\]"),
        "Sybase": (r"(?i)Warning.*sybase.*", r"Sybase message", r"Sybase.*Server message.*"),
    }
    #测试数据库信息
    new_url = url + " %29%28%22%27"
    content = downloader.get(new_url)
    if(content is None):
        print "页面无法打开,请检查网络"
        return False

    for (dbms,regex) in ((dbms,regex) for dbms in DBMS_ERRORS for regex in DBMS_ERRORS[dbms]):
        ret = re.search(regex,content)
        if(ret):
            print "当前网站存在漏洞dbms为",dbms    
            return True
    return False
