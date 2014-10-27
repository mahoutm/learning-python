#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import codecs
import urllib2
import re
from bs4 import BeautifulSoup
import numpy as np


def get_content (url):

        f = urllib2.urlopen(url)
        html = f.read()
        bs = BeautifulSoup(html)

	content = ''
	comments = []

	print 'find content.'
	for line in bs.body.find_all("div", attrs={"class": re.compile("contentBody") }):
                row = []
                for i in line.find_all("p"):
                        row.append(re.sub(r'\s+',' ',i.text.strip()))
                content = re.sub(r'\s+',' ','\n'.join(row)).strip()

	print 'find comment.'
	for line in bs.body.find_all("div", attrs={"class":"commentListInner"}):
	        for i in line.find_all("div", attrs={"class":"replyItem parent_srl_ "}):
	        	row = {}
			for j in i.find_all("div",attrs={"class": "author"}):
				row['author'] = re.sub(r'\s+',' ',j.text.strip())
			for j in i.find_all("div",attrs={"class": "date"}):
				row['date'] = re.sub(r'\s+',' ',j.text.strip())
			for j in i.find_all("div",attrs={"class": "replyContent"}):
	               		row['replyContent'] = re.sub(r'\s+',' ',j.text.strip())
	        	comments.append(row)

        return content,comments

		
def get_board (url):

	f = urllib2.urlopen(url)
	html = f.read()
	bs = BeautifulSoup(html)
	
	docs = []
	
	for line in bs.body.table.tbody.find_all("tr", attrs={"class": re.compile("bg1|bg2") }):
		doc = {}
		key = ''
		for i in line.find_all("td", attrs={"class":"num"}):
			key = re.sub(r'\s+',' ',i.text.strip())
			doc['num'] = key
		for i in line.find_all("td", attrs={"class":"title"}):
			for j in  i.find_all('a'):
				print 'call function.'
				content,comments = get_content(j.get('href'))
                        	doc['content'] = content
                        	doc['comments'] = comments
			doc['title'] = re.sub(r'\s+',' ',i.text.strip())
		for i in line.find_all("td", attrs={"class":"author"}):
			doc['author'] = re.sub(r'\s+',' ',i.text.strip())
		for i in line.find_all("td", attrs={"class":"date"}):
			doc['date'] = re.sub(r'\s+',' ',i.text.strip())
		for i in line.find_all("td", attrs={"class":"recommend"}):
			doc['recommend'] = re.sub(r'\s+',' ',i.text.strip())
		docs.append(doc)
	return docs


if __name__ == "__main__":
	
	#out = get_board('http://www.ilbe.com/index.php?mid=ilbe&page=1')	
	#for i in out:
	#	print i['num'],
	#	print i['title'],
	#	print i['author'],
	#	print i['date'],
	#	print i['recommend']
	#	print '------content-------'
	#	print i['content']
	#	print '------comments------'
	#	for j in i['comments']:
	#		print j['author'],
	#		print j['date'],
	#		print j['replyContent']
	#	print '========================================'

	content, comments = get_content('http://www.ilbe.com/4569410404')
	print content

