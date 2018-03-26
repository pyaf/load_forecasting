import sys,os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()
from swag.models import CSV
import csv, datetime

for i in range(22,24):
    a = 1+i;
    print(a);
    link = "static/SLDC_Data/2018/03/"+str(a).zfill(2)+"-03-2018.csv"
    dataReader = csv.reader(open(link), delimiter=',', quotechar='"')
    for row in dataReader:
        data = CSV.objects.create(timestamp = row[0], load_value = row[1], date = datetime.date(2018,3,a))