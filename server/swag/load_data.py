import sys,os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()
from swag.models import CSV
import csv, datetime

day_range = list(range(0, 31)) # days, 1 to 31

# months, Aug to Dec for 2017, and Jan for 2018
month_range = {
				2017: [8,9,10,11,12],
				2018: [1,2,3]
				}

year_range = [2017,2018]

for year in year_range:
	for month in month_range[year]:
			for day in day_range:
				try:
					a = 1+day
					print(a,month,year);
					link = "static/SLDC_Data/"+str(year)+"/"+str(month).zfill(2)+"/"+str(a).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+".csv"
					dataReader = csv.reader(open(link), delimiter=',', quotechar='"')
					for row in dataReader:
						data = CSV.objects.create(timestamp = row[0], load_value = row[1], date = datetime.date(2018,3,a))
				except Exception as e:
					print(e)