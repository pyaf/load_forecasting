import requests
import csv
import os
from bs4 import BeautifulSoup
url = 'https://www.delhisldc.org/Loaddata.aspx?mode='

day_range = list(range(1, 32)) # days, 1 to 31

# months, Aug to Dec for 2017, and Jan for 2018
month_range = {
				2017: [8,9,10,11,12],
				2018: [1,2,3]
				}

year_range = [2017,2018]

if not os.path.exists('SLDC_Data'):
	    os.makedirs('SLDC_Data')

for year in year_range:
	for month in month_range[year]:
		month_dir = 'SLDC_Data/%d/%02d/' %(year, month)
		if not os.path.exists(month_dir): os.makedirs(month_dir)
		try:
			for day in day_range:
				date = '%02d/%02d/%d' %(day, month, year)
				print('Scraping', date)
				resp = requests.get(url+date) # send a get request to the url, get response
				soup = BeautifulSoup(resp.text, 'lxml') # Yummy HTML soup
				table = soup.find('table', {'id':'ContentPlaceHolder3_DGGridAv'}) # get the table from html
				trs = table.findAll('tr') # extract all rows of the table
				if len(trs[1:])!=0: # no need to create csv file, if there's no data, for Aug month of 2017
					print("ayush")
					csv_filename = month_dir + '%s.csv' % date.replace('/', '-')
					if os.path.exists(csv_filename): os.remove(csv_filename) # remove the file it already exists, can result in data duplicacy
					with open(csv_filename, 'a') as f:
						writer = csv.writer(f)
						for tr in trs[1:]:
							time, delhi = tr.findChildren('font')[:2]
							writer.writerow([time.text, delhi.text])
		except Exception as e:
			print(e)
