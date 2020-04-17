#!/usr/bin/env python3

import json
import time

from time import mktime

f=open("../../data/metaculus.json")
jsondata=json.load(f)

for page in jsondata:
	for question in page["results"]:
		if question["possibilities"]["type"]=="binary" and (question["resolution"]==1 or question["resolution"]==0):
			try:
				restime=time.strptime(question["resolve_time"],"%Y-%m-%dT%H:%M:%S.%fZ")
			except:
				restime=time.strptime(question["resolve_time"],"%Y-%m-%dT%H:%M:%SZ")
			try:
				createtime=time.strptime(question["created_time"],"%Y-%m-%dT%H:%M:%S.%fZ")
			except:
				createtime=time.strptime(question["created_time"],"%Y-%m-%dT%H:%M:%SZ")
			for pred in question["prediction_timeseries"]:
				timediff=mktime(restime)-pred["t"]
				qtimediff=mktime(restime)-mktime(createtime)
				print("{},{},{},{},{}".format(question["id"], qtimediff, question["resolution"], pred["community_prediction"], timediff))
