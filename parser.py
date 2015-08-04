#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' url-html-解析 '

from html.parser import HTMLParser
from html.entities import name2codepoint
from urllib import request

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        #print('<%s>' % tag)
        pass

    def handle_endtag(self, tag):
        #print('</%s>' % tag)
        pass

    def handle_startendtag(self, tag, attrs):
        #print('<%s/>' % tag)
        pass

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        #print('<!--', data, '-->')
        pass

    def handle_entityref(self, name):
        #print('&%s;' % name)
        pass

    def handle_charref(self, name):
        #print('&#%s;' % name)
        pass

with request.urlopen('http://forum.xitek.com/thread-1483336-1-1-1.html') as f:
    data = f.read()
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    body=data.decode('gbk')
    print('Data:', body)

print("NOW 开始解析：")
parser = MyHTMLParser()
parser.feed( body )
