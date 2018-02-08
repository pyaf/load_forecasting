
import sys,os
your_djangoproject_home="django18"
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django18.settings'
from .models import CSV
import csv,datetime
for i in range(30):
    a = 1+i;
    print(a);
    link = "static/SLDC_Data/2017/11/"+str(a).zfill(2)+"-11-2017.csv"
    dataReader = csv.reader(open(link), delimiter=',', quotechar='"')
    for row in dataReader:
        data = CSV()
        data.timestamp = row[0]
        data.load_value = row[1]
        data.date = datetime.date(2017,11,a)
        data.save()
