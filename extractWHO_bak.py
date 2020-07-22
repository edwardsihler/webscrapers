#Edward Sihler
#Extract covid-19 data from the WHO situation reports

# importing required modules 
import PyPDF2 
import sys
import datetime

pdfFileName = '20200402-sitrep-73-covid-19.pdf'

iFile = open("countryList.txt", "r")
countryList = []
countryData = {}
for f in iFile:
	countryList.append(f.strip())

endOfCountry = [' Local transmission ', ' Imported cases only ', 'Local transmission', 'Imported cases only']
multiLine = ['Lao People\'s', 'Northern Mariana','Bosnia and','Iran (Islamic Republic','occupied Palestinian', 'United States of', 'Venezuela (Bolivarian', 'Bolivia (Plurinational', 'Saint Vincent and the','United States Virgin', 'Turks and Caicos', 'Democratic Republic', 'Central African' ]
endMultiLine = ['Democratic Republic']
  
# creating a pdf file object 
pdfFileObj = open(pdfFileName, 'rb')
  
# creating a pdf reader object 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
  
# printing number of pages in pdf file 
#print(pdfReader.numPages) 


foundCountry = False
specialHandling = False
colIndex = 0

for i in range( 1, pdfReader.numPages) :
	pageObj = pdfReader.getPage(i)
	txt = pageObj.extractText()
	ts = txt.split('\n')
	k = 0
	length = len(ts)
	country = {'name':"", 'cases':0, 'deaths':0}
	while k < length :
		t = ts[k].strip() 
		#print("[",t,"]")
		#if t in endOfCountry:
		#	print ("end of Country found")
		#	print('[', t, ']')

		if foundCountry :
			if colIndex == 1:
				country['cases'] = t.strip()
				colIndex += 1
			elif colIndex == 5:
				country['deaths'] = t.strip()
				colIndex += 1
				
			elif t in endOfCountry or colIndex > 5:
				countryData[country['name']] = country
				foundCountry = False
				colIndex = 0

			else :
				colIndex += 1

		if t in countryList:
			foundCountry = True
			country = {'name': t.strip(), 'cases':0, 'deaths':0}
			#country['name'] = t.strip()
			if t in multiLine :
				#print("found multiLine")
				k += 1
				if country['name'] == "Northern Mariana" :
					country['name'] += " " + ts[k].strip() + " " + ts[k+1].strip() + " " + ts[k+2].strip() 
					k += 2
				else :
					country['name'] += " " + ts[k].strip()
			colIndex = 0
			#print(t)
		k += 1
	else :
		continue
	break



 
# closing the pdf file object 
pdfFileObj.close()

#print(countryData)
for c in countryData :
	temp = countryData[c] 
	print(temp['name'], " cases: ", temp['cases'], " deaths: ", temp['deaths']) 

runDate = pdfFileName[0:4]+'/'+pdfFileName[4:6]+'/'+pdfFileName[6:8] + " 10:00:00"

runTime = str(datetime.datetime.now().year) + "/"
runTime += str(datetime.datetime.now().month).zfill(2) + "/"
runTime += str(datetime.datetime.now().day).zfill(2) + " "
runTime += str(datetime.datetime.now().hour).zfill(2) + ":"
runTime += str(datetime.datetime.now().minute).zfill(2) + ":"
runTime += str(datetime.datetime.now().second)


pdfFileName = pdfFileName[:-3] + 'txt'
oFile = open(pdfFileName, "w" )
for c in countryData :
	temp = countryData[c] 
	oString = runDate + "\t" + runTime + "\t" + temp['name'] +"\t" + temp['cases'] + "\t" +temp['deaths'] + "\n"
	oFile.write(oString) 
oFile.close()