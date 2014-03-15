import re
import csv
import json
import urllib2
from bs4 import BeautifulSoup as BS

city = 'Auckland';

def getRoutes(): 
	"""
		Step 1 find possible routes 
	"""
	routes = []
	urlFile = open( city + ".txt", "w" )
	for m in range(100): # 100 miles
		for n in range(1,5): # 5 pages of results
			url = "http://runkeeper.com/search/routes/" + str(n) + "?distance=" + str(m) + "&lon=174.76333150000005&location=" + city + "&activityType=RUN&lat=-36.8484597"
			page = urllib2.urlopen(url).read()
			if page: 
				results = re.findall('user\/[^/]+\/[^/]+\/[^/]+\n', page)
				for k in results:
					route = 'http://runkeeper.com/' + k.replace('">','').replace('\n','')
					if route in routes: 
						print 'duplicate!'
					else:
						print route
						urlFile.write(route)
						urlFile.write('\n')
						routes.append(route)
	urlFile.close()

def getLoc():
	"""
		Step 2 find geo locations 
	"""
	csvFile = csv.writer(open( city + ".csv", "wb+"))
	csvFile.writerow(["tempid","latitude", "longitude"])
	urlFile = open( city + ".txt","r")
	pageID = 0
	for line in urlFile:
		locPage = urllib2.urlopen(line)
		soup = BS(locPage).findAll('script',{"src":False})
		pageID += 1
		print pageID
		for s in soup:
			if 'routePoints' in s.string:
				value = "[{" + s.string.split("}];")[0].split("[{")[1] + "}]"
				jsonObj = json.loads(value)
				for x in jsonObj:
					csvFile.writerow([pageID,x["latitude"],x["longitude"]])
	urlFile.close()

if __name__ == '__main__':
    getRoutes()
    getLoc()