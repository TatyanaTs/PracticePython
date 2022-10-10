from grafana_client import GrafanaApi, HeaderAuth, TokenAuth
from selenium.common.exceptions import TimeoutException
from dateutil import parser
from datetime import datetime
from urllib.parse import quote
import urllib.request
import time
import requests
import shutil
import json

#http://localhost:3000/d/FVt3H34Vk/telegraf-and-influx-windows-host-overview?orgId=1&refresh=1m
host = "http://localhost:3000"

# Url to request for finding all accessible dashboards with basic auth
url = host + "/api/search"
r = requests.get(url, auth=('admin', 'admin'))
print("Url page with all dashboards response status_code is ", r.status_code)

# Start reading url text content which contains multiple JSON objects
jsonText = json.loads(r.text)
# print(r.text)


# Find title (uri) by uid
uid = "FVt3H34Vk"
for item in jsonText:
    if (item['uid'] == uid):
        # print (item['uid'], item['title'])
        uriParts = item['uri'].split("/")
        uri = uriParts[1]
        # print(uriParts)

# Create the url request to find all graphics in dashboard
urlReqDB = host + "/api/dashboards/uid/" + uid
print("URL of dashboard by uid is ", urlReqDB)
reqDB = requests.get(urlReqDB, auth=('admin', 'admin'))
# print("text of reqDB\n", reqDB.text)

# Page content to JSON format
allGraphics = json.loads(reqDB.text)

# Get vars from saved variables in grafana dashboard
# print(allGraphics['dashboard']['time']['from'])

# Get time period
setDatetimeFrom = allGraphics['dashboard']['time']['from']
dateStart = parser.parse(setDatetimeFrom)
timeStart = str(int(time.mktime(dateStart.timetuple()))) + "000"
setDatetimeTo = allGraphics['dashboard']['time']['to']
dateTo = parser.parse(setDatetimeTo)
timeTo = str(int(time.mktime(dateTo.timetuple()))) + "000"
# print(type(timeStart), type(timeTo))
# print(timeStart, timeTo)

# Get variables
varsTitle = allGraphics['dashboard']['templating']['list']
varsNumber = len(varsTitle)
print("Number of db variables is ", varsNumber)
varsName = []
varsValue = []
for item in varsTitle:
    varsName.append(item['name'])
    # Check if value is a string we should convert to array, so loop after can be work without separating it by a letter
    if (type(item['current']['text']) == type("str")):
        varsValue.append([item['current']['text']])
    else:
        varsValue.append(item['current']['text'])
print(varsName, varsValue)

# Count how many panels dashboard has
panelsNumber = allGraphics['dashboard']['panels']
print("This dashboard has " + str(len(panelsNumber)) + " panels")


# Create the url request for Grafana Image Renderer
urlReqGraph = host + "/render/d-solo/" + uid + "/" + uri + "?orgId=1&from=" + timeStart + "&to=" + timeTo + "&theme=light&width=1000&height=500&tz=Europe%2FMoscow&panelId="

headers = [('Authorization', 'Bearer eyJrIjoiYnFBWkVwWTYwa21kc2V3S2QxUGUzc0xWQU83dWM3anoiLCJuIjoiUHl0aG9uIiwiaWQiOjF9')]
opener = urllib.request.build_opener()
opener.addheaders = headers
urllib.request.install_opener(opener)
# for panel in range(panelsNumber):
for panel in panelsNumber:
    if (panel['type'] == "graph"):
        panelId = panel['id']
        urlReqGraphNew = urlReqGraph + str(panelId)
        print(urlReqGraphNew)
        for i in range(len(varsName)):
            for j in range(len(varsValue[i])):
                urlReqGraphNew = urlReqGraphNew + "&var-" + varsName[i] + "=" + varsValue[i][j]
        urlReqGraphNew = urlReqGraphNew.replace(" ", "%20").replace("[", "%5B").replace("]", "%5D")
        print("Panel " + str(panelId) + ": " + urlReqGraphNew)
        urllib.request.urlretrieve(urlReqGraphNew, "D:\\GrafanaImages\\Image_" + str(panelId) + ".png")