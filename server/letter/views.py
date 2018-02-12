from django.shortcuts import render, HttpResponse
from .models import CSV
import datetime
from datetime import timedelta
from django.utils.safestring import mark_safe
import json

# Create your views here.
# from .forms import CSVForm
import requests
import csv
import os
from bs4 import BeautifulSoup



def home(request):
    print("adscvadsfvadsfvadsfa")
    print("date dekh le bhai",datetime.date.today().day)
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    return render(request, "home.html", {'Day': str(day).zfill(2),
                                        'Month': str(month).zfill(2),
                                        'Year': year})

    

def cal(request):
    print("cal");
    if request.method == 'POST':
        # query_results = CSV.objects.filter(date = request.POST['from'])
        a = request.POST['from']
        b = request.POST['to']
        print(a,b)
        print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        ans = a.split('-')
        bns = b.split('-')
        aa = datetime.date(int(ans[0]),int(ans[1]),int(ans[2]))
        bb = datetime.date(int(bns[0]),int(bns[1]),int(bns[2]))
        query_results = []
        last = []
        t = ['x']
        for i in range((bb-aa).days+1):
            print(i ,"ayushJXHDKJHFKJDBH")
            query_results.append(CSV.objects.filter(date = aa+timedelta(days=i)))
            q = [str(aa+timedelta(days=i))]
            for x in query_results[i]:
                q.append(x.load_value)
            last.append(q)
            # print(query_results)
        for x in query_results[0]:
            hour = x.timestamp.hour
            minutes = x.timestamp.minute
            t.append(str(hour)+':'+str(minutes))
        last.insert(0,t)

    else:
        last = None
    print ('sadf',last)
    cont = {
            # "query_results":query_results,
            'Load':last,
            # 'Tarikh':a,
            # 'T':mark_safe(t),
            # 'Load': [x.load_value for x in query_results],
            # 'Time': [x.timestamp for x in query_results],
        }

    return HttpResponse(json.dumps(cont),content_type='application/json')
