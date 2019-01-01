from .models import CSV
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

import sys
import os
djangoproject_home = "website"
sys.path.append(djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'


@periodic_task(run_every=(crontab(minute=55, hour='0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23')), name="reload_task", ignore_result=True)
def reload_task():
    # global size
    print("date:", datetime.date.today().day)
    url = 'http://www.delhisldc.org/Loaddata.aspx?mode='
    day_range = list(range(datetime.date.today().day,
                           datetime.date.today().day+1))  # days, 1 to 31
    # months, Aug to Dec for 2017, and Jan for 2018
    
    month = datetime.date.today().month
    year = datetime.date.today().year

    if not os.path.exists('static/SLDC_Data'):
        os.makedirs('static/SLDC_Data')

    month_dir = 'static/SLDC_Data/%d/%02d/' % (year, month)
    if not os.path.exists(month_dir):
        os.makedirs(month_dir)
    try:
        for day in day_range:
            date = '%02d/%02d/%d' % (day, month, year)
            print('Scraping', date)
            # send a get request to the url, get response
            resp = requests.get(url+date)
            soup = BeautifulSoup(resp.text, 'lxml')  # Yummy HTML soup
            # get the table from html
            table = soup.find(
                'table', {'id': 'ContentPlaceHolder3_DGGridAv'})
            trs = table.findAll('tr')  # extract all rows of the table
            # no need to create csv file, if there's no data, for Aug month of 2017
            if len(trs[1:]) != 0:
                csv_filename = month_dir + \
                    '%s.csv' % date.replace('/', '-')
                if os.path.exists(csv_filename):
                    # remove the file it already exists, can result in data duplicacy
                    os.remove(csv_filename)
                with open(csv_filename, 'a') as f:
                    writer = csv.writer(f)
                    for tr in trs[1:]:
                        time, delhi = tr.findChildren('font')[:2]
                        t = (time.text).split(':')
                        TimE = datetime.time(int(t[0]), int(t[1]))
                        writer.writerow([str(TimE), delhi.text])
                        print(str(TimE))
                        results = []
                        results.append(CSV.objects.filter(
                            date=datetime.date.today(), timestamp=str(TimE)))
                        if (len(results[0]) == 0):
                            print(TimE, delhi.text)
                            data = CSV()
                            data.timestamp = str(TimE)
                            data.load_value = delhi.text
                            data.date = datetime.date.today()
                            data.save()

                    if(datetime.datetime.time(datetime.datetime.now()).hour == 23 and datetime.datetime.time(datetime.datetime.now()).minute >= 55):
                        print(
                            '............................................')
                        start = datetime.time(0, 0)
                        end = datetime.time(23, 55)
                        while(start != end):
                            blanck_val = []
                            blanck_val.append(CSV.objects.filter(
                                date=datetime.date.today(), timestamp=str(start)))
                            if (len(blanck_val[0]) == 0):
                                data = CSV()
                                data.timestamp = str(start)
                                data.load_value = None
                                data.date = datetime.date.today()
                                data.save()
                                writer.writerow([str(start), None])
                                # CSV.objects.filter(date = datetime.date.today(), timestamp = str(start)).update(load_value = None)
                            start = (datetime.datetime.combine(datetime.date(
                                1, 1, 1), start)+timedelta(minutes=5)).time()

    except Exception as e:
        print(e)


