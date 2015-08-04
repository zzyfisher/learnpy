#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' 操作mongo '
__author__ = 'zzyfisher'
import json
from pymongo import MongoClient
import time

from xitekInfo import ThreadInfo,PostInfo,PageInfo,ForumInfo
	
class MongoStore:
	#构造
	def __init__(self):		
		self.conn=b""
		self.db=b""
		
	#打开db
	def open(self):
		self.conn = MongoClient("127.0.0.1",27017)
		self.db = self.conn.xitek
		
	#保存到db-thread（主题）
	def saveThread(self,thread):
		self.db.threads.insert(thread)
	def saveForum(self,forum):
		j= json.dumps(forum, default=lambda forum: forum.__dict__)
		print(j)
		self.db.forums.insert(json.loads(j))
	def savePost(self,post):
		self.db.posts.insert(post)
		
		
if __name__=='__main__':	
	ms = MongoStore()
	ms.open()
	forum = ForumInfo()
	forum.forumId=100
	forum.forumName="测试论坛"
	ms.saveForum(forum)
