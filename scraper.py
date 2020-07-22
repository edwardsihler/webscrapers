import requests
import urllib.request
import time
import pandas as pd
import datetime
import re
from bs4 import BeautifulSoup




url = 'https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html'
rawPage = requests.get(url, verify = False)

soup = BeautifulSoup(rawPage.text, 'html.parser')

table = soup.find_all('table')[0] # Grab the first table
    
#new_table = pd.DataFrame(columns=range(0,3), index = [0]) # I know the size 

Antrim = {'name':"Antrim", 'infected':0, 'deaths':0}
Benzie = {'name':"Benzie", 'infected':0, 'deaths':0}
Grand_Traverse = {'name':"Grand Traverse", 'infected':0, 'deaths':0}
Kalkaska = {'name':"Kalkaska", 'infected':0, 'deaths':0}
Leelanau = {'name':"Leelanau", 'infected':0, 'deaths':0}

counties = [Antrim, Benzie,Grand_Traverse, Kalkaska, Leelanau]


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
	 	
	 	if ofInterest == 1 :
	 		curCounty['infected'] = column.get_text().strip()

	 	if ofInterest == 2 :
	 		curCounty['deaths'] = column.get_text().strip()

	 	ofInterest +=1

	 extractedData.append(curCounty)


#print("Begin diagnostics")

lastupdate = ""
for caption in soup.find_all('caption') :
	if caption.get_text().find("pdate") > -1 :
		#print(caption.get_text())
		*temp, d = caption.get_text().split("pdated")
		d = d.strip()
		
		if re.match("^\d{1,2}/\d{1,2}/\d{4}", d) and len(lastupdate) < 10  :
			
			ds = d.split('/')
			lastupdate = ds[2]  + '/' + ds[0].zfill(2) + '/'  + ds[1].zfill(2) +  " 15:00:01"


if not (re.match("\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}",lastupdate)) :
	lastupdate = str(datetime.datetime.now().year) + "/"
	lastupdate += str(datetime.datetime.now().month).zfill(2) + "/"
	lastupdate += str(datetime.datetime.now().day).zfill(2) + " 00:00:01"
#print(lastupdate)


	 	
runTime = str(datetime.datetime.now().year) + "/"
runTime += str(datetime.datetime.now().month).zfill(2) + "/"
runTime += str(datetime.datetime.now().day).zfill(2) + " "
runTime += str(datetime.datetime.now().hour).zfill(2) + ":"
runTime += str(datetime.datetime.now().minute).zfill(2) + ":"
runTime += str(datetime.datetime.now().second)

extractedData = extractedData[1:-1]

#print(table)

#print("website update DT\trun DT\tCounty\tCumulative Cases\tCumulative Deaths")

#for x in extractedData:
#	print(lastupdate, "\t", runTime, "\t", x['name'], "\t",x['infected'], "\t",x['deaths'])

	 #print(extractedData)
now = datetime.datetime.now()
filename = "new/"+ now.strftime("%Y-%m-%d_%H-%M-%S" ) + ".txt"

oFile = open(filename,"w+")
#oFile.write("website update DT\trun DT\tCounty\tCumulative Cases\tCumulative Deaths\r\n")
for x in extractedData:
	temp = lastupdate + "\t" + runTime + "\t" + x['name'] + "\t" + x['infected'] + "\t" +x['deaths'] + "\r\n"
	oFile.write(temp)

oFile.close()
