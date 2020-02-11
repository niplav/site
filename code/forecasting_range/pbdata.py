import urllib2

from bs4 import BeautifulSoup

import sys
from dateutil.parser import parse

def showforecasts(linkp, res):
	urlp="https://predictionbook.com{}".format(linkp)
	print(linkp)
	reqp=urllib2.Request(urlp, headers={"User-Agent" : "Firefox"})
	try:
		conp=urllib2.urlopen(reqp)
	except urllib2.HTTPError, e:
		return
	datap=conp.read()
	soupp=BeautifulSoup(datap, "html.parser")

	timedata=soupp.find(lambda tag:tag.name=="p" and "Created by" in tag.text)

	#This takes the planned resolution datetime
	#resolved=timedata.find_all("span", class_="date")[1].get("title")
	#This takes the real resolution datetime
	#"date created_at" is a fucking lie, by the way
	#TODO: maybe write a pull request?

	resolved=timedata.find("span", class_="judgement").find("span", class_="date created_at").get("title")
	resobj=parse(resolved)

	responses=soupp.find_all("li", class_="response")
	for r in responses:
		forecasts=r.find_all("span", class_="confidence")
		if forecasts!=[]:
			est=float(r.find_all("span", class_="confidence")[0].text.strip("%"))/100
		else:
			continue
		estime=r.find("span", class_="date").get("title")
		estobj=parse(estime)
		print("{},{},{}".format(res, est, (resobj-estobj).days))

for page in range(240,1000):
	print(page)

	url="https://predictionbook.com/predictions/page/{}".format(page)
	req=urllib2.Request(url, headers={"User-Agent" : "Firefox"})
	try:
		con=urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		break
	data=con.read()
	soup=BeautifulSoup(data, "html.parser")
	predright=soup.find_all("li", {"class": "prediction right"})
	predwrong=soup.find_all("li", {"class": "prediction wrong"})
	for pred in predright:
		linkp=pred.span.a.get("href")
		showforecasts(linkp, "1.0")
	for pred in predwrong:
		linkp=pred.span.a.get("href")
		showforecasts(linkp, "0.0")
