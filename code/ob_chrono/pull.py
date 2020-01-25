import urllib2
from bs4 import BeautifulSoup
import sys
import datetime

for year in range(2006, datetime.datetime.now().year+1):
	yearposts=[]
	for page in range(1, 1000):
		url='http://www.overcomingbias.com/{}/page/{}'.format(year, page)
		req=urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		try:
			con=urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			break
		data=con.read()
		soup=BeautifulSoup(data, 'html.parser')
		posts=soup.find_all(class_="post")
		for p in posts:
			title=p.find_all(class_="entry-title")[0].a.text
			link=p.find_all(class_="entry-title")[0].a.get('href')
			meta=p.find_all(class_="entry-meta")

			# For some reason, BeautifulSoup has a problem with this post: http://www.overcomingbias.com/2012/09/millers-singularity-rising.html
			# Let's ignore it and fix it by hand
			if meta!=[]:
				author=p.find_all(class_="entry-meta")[0].find_all(class_='author')[0].a.text
				date=p.find_all(class_="entry-meta")[0].find_all(class_='entry-date')[0].text
			else:
				author=""
				date=""
			entry='* [{}]({}) ({}, {})'.format(title.encode('utf_8'), str(link), str(author), str(date))
			yearposts.append(entry)
	print('\n### {}\n'.format(year))
	for t in reversed(yearposts):
		print(t)
