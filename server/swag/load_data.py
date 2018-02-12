
import sys,os
djangoproject_home="website"
sys.path.append(djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
from .models import CSV
import csv,datetime
for i in range(10,11):
    a = 1+i;
    print(a);
    link = "static/SLDC_Data/2018/02/"+str(a).zfill(2)+"-02-2018.csv"
    dataReader = csv.reader(open(link), delimiter=',', quotechar='"')
    for row in dataReader:
        data = CSV()
        data.timestamp = row[0]
        data.load_value = row[1]
        data.date = datetime.date(2018,2,a)
        data.save()
