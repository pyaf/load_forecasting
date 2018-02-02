import requests
import csv
import os
from bs4 import BeautifulSoup
url = 'https://www.wunderground.com/history/airport/VIDP/%d/%d/%d/DailyHistory.html'

day_range = list(range(1, 32)) # days, 1 to 31

# months, Aug to Dec for 2017, and Jan for 2018
month_range = {
				2017: list(range(8, 13)),
				2018: [1]
				}

year_range = [2017, 2018]

if not os.path.exists('Whether_Data'):
	    os.makedirs('Whether_Data')

columns = ['time', 'temp', 'heat index', 'dew point', 'humidity',
			 'pressure', 'visibility', 'wind dir', 'wind speed', 
			 'gust speed', 'precip', 'events', 'conditions']

for year in year_range:
	for month in month_range[year]:
		month_dir = 'Whether_Data/%d/%02d/' %(year, month)
		if not os.path.exists(month_dir): os.makedirs(month_dir)
		try:
			for day in day_range:
				date = '%02d/%02d/%d' %(day, month, year)
				print('Scraping', date)
				resp = requests.get(url % (year, month, day)) # send a get request to the url, get response
				soup = BeautifulSoup(resp.text, 'lxml') # Yummy HTML soup
				table = soup.find('table', {'id':'obsTable'}) # get the table from html
				trs = table.findAll('tr') # extract all rows of the table
				if len(trs[1:])!=0: # no need to create csv file, if there's no data, for Aug month of 2017
					csv_filename = month_dir + '%s.csv' % date.replace('/', '-')
					if os.path.exists(csv_filename): os.remove(csv_filename) # remove the file it already exists, can result in data duplicacy
					with open(csv_filename, 'a') as f:
						writer = csv.writer(f)
						writer.writerow(columns)
						for tr in trs[1:]:
							row = []
							tds = tr.findChildren('td')
							for td in tds:
								span = td.findChildren('span', {'class':'wx-value'})
								if span:
									row.append(span[0].text.strip())
								else:
									row.append(td.text.strip())
							assert (len(row) == len(columns))
							writer.writerow(row)
		except Exception as e:
			print(e)
			print(date)