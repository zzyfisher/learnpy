#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' BS4-解析 '

from bs4 import BeautifulSoup
from urllib import request
import re

with request.urlopen('http://forum.xitek.com/thread-1482407-1-1-1.html') as f:
    data = f.read()
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    body=data.decode('gbk')
#    print('Data:', body)

soup = BeautifulSoup(body,"html.parser")
#print (soup.prettify())

#postlist=soup.find("div",id='postlist')
tablelist=soup.find_all("table",id=re.compile('^pid'))
#soup.find_all(href=re.compile("elsie"), id='link1')

#print(tablelist)

print("\n+++++")
#现在开始解析发帖子的信息（用户，发帖时间，更新时间，帖子内容）
for t in tablelist:		
	#用户:第一个 <td class="pls"
	u = t.find("td",attrs={"class":"pls"})
	#print ("user:"+ u.prettify())
	
	#用正则处理用户信息
	'''
	<td class="pls" nowrap="" valign="top" width="120">
	<font class="allb" size="3"><a href="/space-uid-1843865.html" target="_blank"><b>maomaodada1979</b></a></font>
	<br/>
	<font color="black" id="small9">
	泡菜 <img alt="邮箱已验证" border="0" src="static/image/common/mailverified.gif" title="邮箱已验证" width="16px"/>
	<br/>
	                        泡网分: 0.077<br/>
	主题: 1<br/>
	帖子: 52<br/>
	注册: 2011年12月<br/>
	</font>
	</td>
	'''
	pattern = re.compile(r"<b>(.*?)</b>.*?注册: (.*?)<br/>",re.S)
	msg=u.prettify()
	v1=re.findall(pattern,msg)
	#print(v)

	#用正则处理内容信息
	#内容
	m = t.find("td",id=re.compile('^postmessage_'))	
	#print("message:" + m.prettify())
	
	pattern = re.compile(r"<td .*?>(.*?)</td>",re.S)
	msg=m.prettify()
	v2=re.findall(pattern,msg)
	#print(v)

	print("x" v1[0]+","+ v1[1]+","+ v2[0])
