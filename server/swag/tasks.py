from celery.task.schedules import crontab
from celery.decorators import periodic_task

from random import randint
# Create your views here.
# from .forms import CSVForm

import datetime
from datetime import timedelta
import requests
import csv
import os
from bs4 import BeautifulSoup

import sys,os
djangoproject_home="website"
sys.path.append(djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
from .models import CSV
import csv,datetime

# from .views import forecasted_plot

# @periodic_task(run_every=(crontab(minute='*/1')), name="update_database", ignore_result=True

# size=0

@periodic_task(run_every=(crontab(minute=55, hour='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23')), name="reload_task", ignore_result=True)
def reload_task():
	# global size
	print("date dekh le bhai",datetime.date.today().day)
	url = 'https://www.delhisldc.org/Loaddata.aspx?mode='
	day_range = list(range(datetime.date.today().day,datetime.date.today().day+1)) # days, 1 to 31
	# months, Aug to Dec for 2017, and Jan for 2018
	month_range = {
					# 2017: list(range(12, 13)),
					2018: [datetime.date.today().month]
					}

	year_range = [datetime.date.today().year]

	if not os.path.exists('static/SLDC_Data'):
		os.makedirs('static/SLDC_Data')

	for year in year_range:
		for month in month_range[year]:
			month_dir = 'static/SLDC_Data/%d/%02d/' %(year, month)
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
						csv_filename = month_dir + '%s.csv' % date.replace('/', '-')
						if os.path.exists(csv_filename): os.remove(csv_filename) # remove the file it already exists, can result in data duplicacy
						with open(csv_filename, 'a') as f:
							writer = csv.writer(f)
							# writer.writerow(['x', 'y'])
							for tr in trs[1:]:
								time, delhi = tr.findChildren('font')[:2]
								t = (time.text).split(':')
								TimE = datetime.time(int(t[0]),int(t[1]))
								writer.writerow([str(TimE), delhi.text])
								print(str(TimE))
								
								results=[]
								results.append(CSV.objects.filter(date = datetime.date.today(), timestamp = str(TimE)))
								# print("hhhhhhhhhhheeeee", len(results[0]))
								if (len(results[0]) == 0):
									# for z in results[0]:
									#	print (z.timestamp, type(z.timestamp), len(results))
									print(TimE, delhi.text)
									data = CSV()
									data.timestamp = str(TimE)
									data.load_value = delhi.text
									data.date = datetime.date.today()
									data.save()

							if(datetime.datetime.time(datetime.datetime.now()).hour == 23 and datetime.datetime.time(datetime.datetime.now()).minute >= 55):
								print('............................................')
								# x = '00:00:00'
								start = datetime.time(0,0)
								end = datetime.time(23,55)
								# size_reduction = 0
								while(start != end):
									# tym = x.split(':')
									# Time = datetime.time(int(tym[0]),int(tym[1]))
									# print((datetime.datetime.combine(datetime.date(1,1,1),Time)+timedelta(minutes=5)).time())
									blanck_val=[]
									blanck_val.append(CSV.objects.filter(date = datetime.date.today(), timestamp = str(start)))
									# print("hhhhhhhhhhheeeee", len(results[0]))
									if (len(blanck_val[0]) == 0):
										data = CSV()
										data.timestamp = str(start)
										data.load_value = None
										data.date = datetime.date.today()
										data.save()
										writer.writerow([str(start), None])
										# CSV.objects.filter(date = datetime.date.today(), timestamp = str(start)).update(load_value = None)
									start = (datetime.datetime.combine(datetime.date(1,1,1),start)+timedelta(minutes=5)).time()

			except Exception as e:
				print(e)

	# link = "static/SLDC_Data/"+ str(year) + "/"+ str(month).zfill(2) + "/" + str(day).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year) +".csv"
	# # link = "static/SLDC_DataBase/2017/11/"+str(a).zfill(2)+"-11-2017.csv"
	# dataReader = csv.reader(open(link), delimiter=',', quotechar='"')
	# rows = list(dataReader)
	# print(len(rows))
	# print(rows)
	# print("global k baad",size)
	# # if(len(rows) > size):
	# print(len(rows))
	# print(size_reduction)
	# for row in rows[size:len(rows)+1]:
	# 	print("inside 2")
	# 	data = CSV()
	# 	if(row[1]=='None'):
	# 		break
	# 	print('row[0]',row[0])
	# 	data.timestamp = row[0]
	# 	data.load_value = row[1]
	# 	data.date = datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
	# 	data.save()
	# size = len(rows)-size_reduction
	# if(datetime.datetime.time(datetime.datetime.now()).hour == 23 and datetime.datetime.time(datetime.datetime.now()).minute >= 40):
	# 	size = 0
	# print("final wali........end",size)
	# print("update_done...............yupppp")



# def update_database():
# 	print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
	# for i in range(30):
	# 	a = 1+i;
	# 	print(a);
	# print("000000000000000000000000mmmmmmmmmmm")
	# print("adscvadsfvadsfvadsfa")
	# print("date dekh le bhai",datetime.date.today().day)
	# url = 'https://www.delhisldc.org/Loaddata.aspx?mode='
	# day_range = list(range(datetime.date.today().day,datetime.date.today().day+1)) # days, 1 to 31
	# # months, Aug to Dec for 2017, and Jan for 2018
	# month_range = {
	#                 # 2017: list(range(12, 13)),
	#                 2018: [datetime.date.today().month]
	#                 }

	# year_range = [datetime.date.today().year]

	# if not os.path.exists('static/SLDC_DataBase'):
	#         os.makedirs('static/SLDC_DataBase')

	# for year in year_range:
	#     for month in month_range[year]:
	#         month_dir = 'static/SLDC_DataBase/%d/%02d/' %(year, month)
	#         if not os.path.exists(month_dir): os.makedirs(month_dir)
	#         try:
	#             for day in day_range:
	#                 date = '%02d/%02d/%d' %(day, month, year)
	#                 print('Scraping', date)
	#                 resp = requests.get(url+date) # send a get request to the url, get response
	#                 soup = BeautifulSoup(resp.text, 'lxml') # Yummy HTML soup
	#                 table = soup.find('table', {'id':'ContentPlaceHolder3_DGGridAv'}) # get the table from html
	#                 trs = table.findAll('tr') # extract all rows of the table
	#                 if len(trs[1:])!=0: # no need to create csv file, if there's no data, for Aug month of 2017
	#                     csv_filename = month_dir + '%s.csv' % date.replace('/', '-')
	#                     if os.path.exists(csv_filename): os.remove(csv_filename) # remove the file it already exists, can result in data duplicacy
	#                     with open(csv_filename, 'a') as f:
	#                         writer = csv.writer(f)
	#                         # writer.writerow(['x', 'y'])
	#                         for tr in trs[1:]:
	#                             time, delhi = tr.findChildren('font')[:2]
	#                             writer.writerow([time.text, delhi.text])
	#         except Exception as e:
	#             print(e)
	# print("done updating")
	# link = "/static/SLDC_DataBase/"+ year + "/"+ month + "/" + day + "-" + month + "-" + year +".csv"
	# # link = "static/SLDC_DataBase/2017/11/"+str(a).zfill(2)+"-11-2017.csv"
	# dataReader = csv.reader(open(link), delimiter=',', quotechar='"')
	# for row in dataReader:
	# 	data = CSV()
	# 	data.timestamp = row[0]
	# 	data.load_value = row[1]
	# 	data.date = datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
	# 	data.save()
	# print("update_done...............yupppp")
