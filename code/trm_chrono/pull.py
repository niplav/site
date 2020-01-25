import urllib2
from bs4 import BeautifulSoup
import sys
import datetime

for year in range(2013, datetime.datetime.now().year+1):
	yearposts=[]
	for page in range(1, 1000):
		url='https://therealmovement.wordpress.com/{}/page/{}'.format(year, page)
		req=urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		try:
			con=urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			break
		data=con.read()
		soup=BeautifulSoup(data, 'html.parser')
		posts=soup.find_all(class_="post")
		for p in posts:
			ts=p.find_all(class_="entry-title")
			if ts==[]:
				break
			title=p.find_all(class_="entry-title")[0].a.text
			link=p.find_all(class_="entry-title")[0].a.get('href')
			date=p.h5.text[1:]
			entry='* [{}]({}) (Jehu, {})'.format(title.encode('utf_8'), str(link), str(date))
			yearposts.append(entry)
	print('\n### {}\n'.format(year))
	for t in reversed(yearposts):
		print(t)
