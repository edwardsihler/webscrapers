import requests
import urllib.request
import time
import pandas as pd
import datetime
from bs4 import BeautifulSoup



lastupdate = ""
for caption in soup.find_all('caption') :
	if caption.get_text().find("Update") > -1 :
		print(caption.get_text())
		*temp, d, t = caption.get_text().split()
		print(d, " :: ", t)
		ds = d.split('/')
		lastupdate = ds[2] + '/'  + ds[1] + '/' + ds[0] +  " " + t


print(lastupdate)
	 	
runTime = str(datetime.datetime.now().year) + "/"
runTime += str(datetime.datetime.now().month) + "/"
runTime += str(datetime.datetime.now().day) + "/ "
runTime += str(datetime.datetime.now().hour) + ":"
runTime += str(datetime.datetime.now().minute) + ":"
runTime += str(datetime.datetime.now().second)


url = 'https://experience.arcgis.com/experience/685d0ace521648f8a5beeeee1b9125cd'

# or https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/
rawPage = requests.get(url)

soup = BeautifulSoup(rawPage.text, 'html.parser')

table = soup.find_all('table')[0] # Grab the first table
    



extractedData = []

for row in table.find_all('tr'):

	 columns = row.find_all('td')
	 ofInterest = 0
	 curCounty = {'name':"", 'infected':0, 'deaths':0}
	 for column in columns:

	 	xs = column.get_text().split('\n')
	 	
	 	if ofInterest == 0 :
	 		curCounty['name']= column.get_text().strip()
	 		#print (curCounty['name'])
	 	
	 	if ofInterest == 2 :
	 		curCounty['infected'] = column.get_text().strip()

	 	if ofInterest == 1 :
	 		curCounty['deaths'] = column.get_text().strip()

	 	ofInterest +=1

	 extractedData.append(curCounty)


print("Begin diagnostics")

lastupdate = ""
for caption in soup.find_all('caption') :
	if caption.get_text().find("Update") > -1 :
		print(caption.get_text())
		*temp, d, t = caption.get_text().split()
		print(d, " :: ", t)
		ds = d.split('/')
		lastupdate = ds[2] + '/'  + ds[1] + '/' + ds[0] +  " " + t


print(lastupdate)
	 	
runTime = str(datetime.datetime.now().year) + "/"
runTime += str(datetime.datetime.now().month) + "/"
runTime += str(datetime.datetime.now().day) + "/ "
runTime += str(datetime.datetime.now().hour) + ":"
runTime += str(datetime.datetime.now().minute) + ":"
runTime += str(datetime.datetime.now().second)



#print(table)

#print("website update DT\trun DT\tCounty\tCumulative Cases\tCumulative Deaths")
##extractedData = extractedData[1:-1]
#for x in extractedData:
#	print(lastupdate, "\t", runTime, "\t", x['name'], "\t",x['infected'], "\t",x['deaths'])

	 #print(extractedData)
oFile = open("mi_Covid19_data.txt","a+")
oFile.write("website update DT\trun DT\tCounty\tCumulative Cases\tCumulative Deaths\r\n")
for x in extractedData:
	temp = lastupdate + "\t" + runTime + "\t" + x['name'] + "\t" + x['infected'] + "\t" +x['deaths'] + "\r\n"
	oFile.write(temp)

oFile.close()
