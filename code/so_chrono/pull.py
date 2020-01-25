import urllib2
from bs4 import BeautifulSoup
import sys
import datetime

author='Scott Aaronson'

for year in range(2005, datetime.datetime.now().year+1):
	yearposts=[]
	for page in range(1, 100):
		url='https://www.scottaaronson.com/blog/?m={}1&paged={}'.format(year, page)
		req=urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		try:
			con=urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			break
		data=con.read()
		soup=BeautifulSoup(data, 'html.parser')
		posts=soup.find_all(class_="post")
		for p in posts:
			title=p.h3.text
			link=p.h3.a.get('href')
			date=p.small.text
			entry='* [{}]({}) ({}, {})'.format(title.encode('utf_8'), str(link), str(author), str(date))
			yearposts.append(entry)
	print('\n### {}\n'.format(year))
	for t in reversed(yearposts):
		print(t)
