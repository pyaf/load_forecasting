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



def home_page(request):
    print("adscvadsfvadsfvadsfa")
    print("date dekh le bhai",datetime.date.today().day)
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    return render(request, "Home_page.html", {'Day': str(day).zfill(2),
                                        'Month': str(month).zfill(2),
                                        'Year': year})

def graph_plot(request):
    print("insde graph_plot");
    if request.method == 'POST':
        print(request.POST)
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
    # print ('sadf',last)
    cont = {
            # "query_results":query_results,
            'Load':last,
            # 'Tarikh':a,
            # 'T':mark_safe(t),
            # 'Load': [x.load_value for x in query_results],
            # 'Time': [x.timestamp for x in query_results],
        }

    return HttpResponse(json.dumps(cont),content_type='application/json')


def forecasted_plot(request):
    print("insde forecasted_plot");
    if request.method == 'POST':
        # query_results = CSV.objects.filter(date = request.POST['from'])
        # if 'fc' in request.POST:
        #     qq = request.POST['fc']
        # else:
        #     qq = False
        # a = request.POST.get('fc', False)
        print(request.POST)
        qq = request.POST['fc']
        p=5
        print(qq)
        print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
        ans = qq.split('-')
        # bns = b.split('-')
        aa = datetime.date(int(ans[0]),int(ans[1]),int(ans[2]))
        # bb = datetime.date(int(bns[0]),int(bns[1]),int(bns[2])-p)
        query_results = []
        last = []
        l = []
        t = ['x']
        for i in range(p+1):
            print(i ,"ayushJXHDKJHFKJDBH")
            query_results.append(CSV.objects.filter(date = aa-timedelta(days=i)))
            q = [str(aa-timedelta(days=i))]
            for x in query_results[i]:
                q.append(x.load_value)
            last.append(q)
        # print(len(q))
        # print(last[1])
        # print(q)
        weights = [0.4, 0.2, 0.15, 0.15, 0.1]
        weights_load = ['forecasted with wmavg']
        simple_load = ['forecasted with smavg']
        for i in range(1,289):
            init = 0
            init1 = 0
            no_of_data = 0
            total_weight = 0
            for j in range(1,p+1):
                try:
                    # print(j)
                    init += last[j][i]
                    # print(weights[j-1],last[j][i])
                    init1 += weights[j-1]*last[j][i]
                    no_of_data = no_of_data+1
                    total_weight = total_weight+weights[j-1]
                except Exception as e:
                    print(e)
                # print(last[j][i])
            # print()
            # print(total_weight,no_of_data)
            weights_load.append("%.2f" % (init1/total_weight))
            simple_load.append("%.2f" % (init/no_of_data))
        # print(w)
        l.append(simple_load)
        l.append(weights_load)
        l.append(last[0])
            # print(query_results)
        for x in query_results[p]:
            hour = x.timestamp.hour
            minutes = x.timestamp.minute
            t.append(str(hour)+':'+str(minutes))
        l.insert(0,t)

    else:
        l = None
    # print ('sadf',w)
    cont = {
            # "query_results":query_results,
            'forecasted_Load':l,
            # 'Tarikh':a,
            # 'T':mark_safe(t),
            # 'Load': [x.load_value for x in query_results],
            # 'Time': [x.timestamp for x in query_results],
        }

    return HttpResponse(json.dumps(cont),content_type='application/json')
