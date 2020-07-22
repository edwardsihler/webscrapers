#Edward Sihler
#Extract covid-19 data from the WHO situation reports

# importing required modules 
import PyPDF2 
import sys
import datetime
import getopt



def extractData (pdfFileName, countryFileName):

	#pdfFileName = '20200402-sitrep-73-covid-19.pdf'

	iFile = open(countryFileName, "r")
	countryList = []
	countryData = {}
	for f in iFile:
		countryList.append(f.strip())

	endOfCountry = [' Local transmission ', ' Imported cases only ', 'Local transmission', 'Imported cases only']
	multiLine = ['Lao People\'s', 'Northern Mariana','Bosnia and', 'Dominican', 'El','Iran (Islamic Republic','occupied Palestinian', 'United States of', 
	'Venezuela (Bolivarian', 'Bolivia (Plurinational', 'Saint Vincent and the','United States Virgin', 'Turks and Caicos', 
	'Democratic Republic', 'Central African','International', 'San', 'United Republic of']
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
			if t == "Guinea":
				print(t) 
			#print("[",t,"]")
			#if t in endOfCountry:
			#	print ("end of Country found")
			#	print('[', t, ']')

			if foundCountry :
				if colIndex == 1:
					if t.strip() == "Bissau" :
						country['name'] = country['name'] + "-Bissau"
						country['cases'] = ts[k+2].strip()
						country['deaths'] = ts[k+4].strip()
						k+=4
						countryData[country['name']] = country
						foundCountry = False
						colIndex = 0
					elif country['name'] == 'Kosovo' :
						country['cases'] = ts[k+2].strip()
						country['deaths'] = ts[k+6].strip()
						countryData[country['name']] = country
						foundCountry = False
						k+=6
					elif country['name'] == 'Cabo' :
						country['name'] = 'Cabo Verde'
						country['cases'] = ts[k+2].strip()
						country['deaths'] = ts[k+6].strip()
						countryData[country['name']] = country
						foundCountry = False
						#print ("|" + ts[k+1].strip() + "|" + ts[k+2].strip() +"|" + ts[k+3].strip() +"|" + ts[k+4].strip() +"|" + ts[k+5].strip() )
						k+=6
					elif country['name'] == 'Cura' :
						country['name'] = 'Curaçao'
						country['cases'] = ts[k+3].strip()
						country['deaths'] = ts[k+5].strip()
						countryData[country['name']] = country
						foundCountry = False
						#print ("|" + ts[k+1].strip() + "|" + ts[k+2].strip() +"|" + ts[k+3].strip() +"|" + ts[k+4].strip() +"|" + ts[k+5].strip() )
						k+=6

						
					elif country['name'] == 'Tanzania' :
						if not t.strip().isdigit() :
							foundCountry = False
							colIndex = 0
								
					else :
						country['cases'] = t.strip()
						country['deaths'] = ts[k+4].strip()
						#print ("|" + ts[k+1].strip() + "|" + ts[k+2].strip() +"|" + ts[k+3].strip() +"|" + ts[k+4].strip() +"|" + ts[k+5].strip() )
						k+=4
						countryData[country['name']] = country
						foundCountry = False
						colIndex = 0
					
				elif t in endOfCountry or colIndex > 5:
					countryData[country['name']] = country
					foundCountry = False
					colIndex = 0

				else :
					colIndex += 1

			if t in countryList:
				foundCountry = True
				country = {'name': t.strip(), 'cases':0, 'deaths':0}
				#if t == "Cabo Verde":
				#print(t)
				#country['name'] = t.strip()
				if t in multiLine :
					#print("found multiLine")
					k += 1
					if country['name'] == "Northern Mariana" :
						country['name'] += " " + ts[k].strip() + " " + ts[k+1].strip() + " " + ts[k+2].strip() 
						k += 2
					if country['name'] == 'International' :
						country['name'] += " " + ts[k].strip() + " " + ts[k+1].strip()
						k += 1
					else :
						country['name'] += " " + ts[k].strip()
				colIndex = 0
				#print(t)
			else :
				print("Is it a country [", t, "]")
			k += 1
		else :
			continue
		break



	 
	# closing the pdf file object 
	pdfFileObj.close()

	#print(countryData)
	#for c in countryData :
		#temp = countryData[c] 
		#print(temp['name'], " cases: ", temp['cases'], " deaths: ", temp['deaths']) 

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


def main(argv):
	pdfFileName = ""
	countryFile = ""

	try:
		opts, args = getopt.getopt(argv,"hp:c:",["pdfFile=","countryFile="])
	except getopt.GetoptError :
   		print ("I need -p the_pdf_file_to_read.pdf -c the_country_file_to_read.txt")
   		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print ("I need -p the_pdf_file_to_read.pdf -c the_country_file_to_read.txt")
			sys.exit()

		elif opt in ("-p", "--pdfFile"):
			pdfFileName = arg

		elif opt in ("-c", "--countryFile"):
			countryFile = arg

	#print ('PDF file is ' + pdfFileName)
	#print ('Country File file is ' + countryFile)
	extractData(pdfFileName, countryFile)
	

if __name__ == '__main__':
	main(sys.argv[1:])