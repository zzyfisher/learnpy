#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'zzyfisher'


import re

pattern = re.compile(r'<table>(.*)</table')
print( re.findall(pattern,"<body><table><tr><td>xxx</td></tr></table>"))


