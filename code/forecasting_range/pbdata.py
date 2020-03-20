#!/usr/bin/env python2

import urllib2
import sys
import time

from bs4 import BeautifulSoup
from time import mktime

def showforecasts(linkp, res):
	urlp="https://predictionbook.com{}".format(linkp)
	reqp=urllib2.Request(urlp, headers={"User-Agent" : "Firefox"})
	try:
		conp=urllib2.urlopen(reqp)
	except (urllib2.HTTPError, urllib2.URLError) as e:
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
	restime=time.strptime(resolved,"%Y-%m-%d %H:%M:%S UTC")

	responses=soupp.find_all("li", class_="response")
	for r in responses:
		forecasts=r.find_all("span", class_="confidence")
		if forecasts!=[]:
			est=float(r.find_all("span", class_="confidence")[0].text.strip("%"))/100
		else:
			continue
		estimated=r.find("span", class_="date").get("title")
		esttime=time.strptime(estimated,"%Y-%m-%d %H:%M:%S UTC")
		print("{},{},{}".format(res, est, mktime(restime)-mktime(esttime)))

for page in range(1,400):
	url="https://predictionbook.com/predictions/page/{}".format(page)
	req=urllib2.Request(url, headers={"User-Agent" : "Firefox"})
	try:
		con=urllib2.urlopen(req)
	except (urllib2.HTTPError, urllib2.URLError) as e:
		continue
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
