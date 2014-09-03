# ingest data and count each words and throw result to postgesql

import codecs
import urllib2
from bs4 import BeautifulSoup

# get a site page
site = 'http://www.auction.co.kr'

f = urllib2.urlopen(site)
html_doc = f.read()

result = []

soup = BeautifulSoup(html_doc)

# get the level 2 deep's pages
for link in soup.find_all('a'):
        link_tmp = link.get('href')
        try:
                f = urllib2.urlopen(link_tmp)
                html_doc = f.read()
                soup = BeautifulSoup(html_doc)
                for str in soup.body.strings:
                        result.append(str)
        except:
                pass

# would be count as unique word
wordcount={}

for line in result:
        for word in line.split():
                if word not in wordcount:
                        wordcount[word] = 1
                else:
                        wordcount[word] += 1

f.close()

#with codecs.open('get.txt','w',encoding='utf8') as f:
#        for word,cnt in wordcount.items():
#                f.write("%s     %d\n" % (word,cnt))

# throwing the result to postgresql (ant)

import psycopg2

try:
    conn = psycopg2.connect("dbname='ant' user='ant' host='zoo' password='ant'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

for word, cnt in wordcount.items():
        cur.execute("INSERT INTO commerce(tm,site,lev,word,cnt) VALUES (now(),%s,2,%s, %s)", (site,word,cnt,) )

conn.commit()
conn.close()
