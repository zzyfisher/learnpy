#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' 处理一个具体的帖子 '

from bs4 import BeautifulSoup
from urllib import request
import re

#帖子信息结构	
class PostInfo:
	threadId=0
	postId=0
	content=""
	uid=""
	uname=""
	postDate=""

class XitekThreadParser:
	url="http://forum.xitek.com/thread-{threadId}-{pageNum}-1-1.html"
	
	#抓取页面数据
	def fetchPage(self,threadId,pageNum):
		purl = self.url.replace("{threadId}",threadId)
		purl = purl.replace("{pageNum}",str(pageNum))
		print (purl)	
		with request.urlopen(purl) as f:
			data = f.read()
			#print('Status:', f.status, f.reason)
			#for k, v in f.getheaders():
			#	print('%s: %s' % (k, v))
			body=data.decode('gbk')
		return body

	#解析
	def parsePage(self,pageData):
		soup = BeautifulSoup(pageData,"html.parser")
		#print (soup.prettify())

		#postlist=soup.find("div",id='postlist')
		tablelist=soup.find_all("table",id=re.compile('^pid'))
	
		retList = []
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
			postInfo = PostInfo()
			postInfo.threadId=threadId

			pattern = re.compile(r"<b>(.*?)</b>.*?注册: (.*?)<br/>",re.S)
			msg=u.prettify()
			v=re.findall(pattern,msg)
			postInfo.uname=v[0][0].strip()


			#用正则处理内容信息
			#内容
			m = t.find("td",id=re.compile('^postmessage_'))	
			#print("message:" + m.prettify())
			
			pattern = re.compile(r"<td .*?>(.*?)</td>",re.S)
			msg=m.prettify()
			v=re.findall(pattern,msg)

			postInfo.content=v[0].strip()
			retList.append(postInfo)

		#处理分页(页面中有2个alln class，都是分页区域)
		'''
		<span class=alln>
		<div class="pg">
		<a href="thread-1482195-1-1-1.html" class="prev">&nbsp;&nbsp;</a>
		<a href="thread-1482195-1-1-1.html">1</a>
		<strong>2</strong>
		</div>
		</span>
		'''
		pageSpan=soup.find("span",attrs={"class":"alln"})
		#print(pageSpan)
		#定位其中最大一个<a>即为页数，如果没有，那么当前页就是最后页，如果找到的最后页数小于当前页，则当前页也是最后页
		listA=pageSpan.find_all("a")
		maxPage=pageNum
		for a in listA:
			href = a.get('href')
			#print("PAGE:" + href)
			sp = href.split("-")
			if int (sp[2]) >maxPage:
				maxPage=int(sp[2])

		return (retList,maxPage)

#执行		
if __name__=='__main__':
	#http://forum.xitek.com/thread-1482195-2-1-1.html
	threadId="1483437"
	#遍历一个forum
	pageNum =1
	threadParser =  XitekThreadParser()
	pageData= threadParser.fetchPage(threadId,pageNum)
	ret = threadParser.parsePage(pageData)
	postList=ret[0]
	maxPage=ret[1]

	print("====Page:%s/%s"%(pageNum,maxPage))
	for p in postList:
			print (p.threadId+","+p.uname+",\n")


	for num in range(2,maxPage+1):
		pageData= threadParser.fetchPage(threadId,num)
		ret = threadParser.parsePage(pageData)
		postList=ret[0]
		print("====Page:%s/%s"%(num,maxPage))
		for p in postList:
			print (p.threadId+","+p.uname+",\n")

