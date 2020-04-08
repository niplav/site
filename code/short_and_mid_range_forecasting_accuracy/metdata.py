#!/usr/bin/env python3

import json
import time

from time import mktime

#Converted via jq -s '[.]|flatten' </usr/local/src/metaculus/data-questions-raw.json >data/metaculus.json
#using data from https://github.com/gimpf/metaculus-question-stats
f=open("../../data/metaculus.json")
jsondata=json.load(f)

for page in jsondata:
	for question in page["results"]:
		if question["possibilities"]["type"]=="binary" and (question["resolution"]==1 or question["resolution"]==0):
			try:
				restime=time.strptime(question["resolve_time"],"%Y-%m-%dT%H:%M:%S.%fZ")
			except:
				restime=time.strptime(question["resolve_time"],"%Y-%m-%dT%H:%M:%SZ")
			for pred in question["prediction_timeseries"]:
				timediff=mktime(restime)-pred["t"]
				print("{},{},{},{}".format(question["id"], question["resolution"], pred["community_prediction"], timediff))
