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
        # t = ['x']
        t = ['x', '00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30', '00:35', '00:40', '00:45', '00:50', '00:55', '01:00', '01:05', '01:10', '01:15', '01:20', '01:25', '01:30', '01:35', '01:40', '01:45', '01:50', '01:55', '02:00', '02:05', '02:10', '02:15', '02:20', '02:25', '02:30', '02:35', '02:40', '02:45', '02:50', '02:55', '03:00', '03:05', '03:10', '03:15', '03:20', '03:25', '03:30', '03:35', '03:40', '03:45', '03:50', '03:55', '04:00', '04:05', '04:10', '04:15', '04:20', '04:25', '04:30', '04:35', '04:40', '04:45', '04:50', '04:55', '05:00', '05:05', '05:10', '05:15', '05:20', '05:25', '05:30', '05:35', '05:40', '05:45', '05:50', '05:55', '06:00', '06:05', '06:10', '06:15', '06:20', '06:25', '06:30', '06:35', '06:40', '06:45', '06:50', '06:55', '07:00', '07:05', '07:10', '07:15', '07:20', '07:25', '07:30', '07:35', '07:40', '07:45', '07:50', '07:55', '08:00', '08:05', '08:10', '08:15', '08:20', '08:25', '08:30', '08:35', '08:40', '08:45', '08:50', '08:55', '09:00', '09:05', '09:10', '09:15', '09:20', '09:25', '09:30', '09:35', '09:40', '09:45', '09:50', '09:55', '10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45', '10:50', '10:55', '11:00', '11:05', '11:10', '11:15', '11:20', '11:25', '11:30', '11:35', '11:40', '11:45', '11:50', '11:55', '12:00', '12:05', '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45', '12:50', '12:55', '13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55', '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', '14:40', '14:45', '14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', '15:30', '15:35', '15:40', '15:45', '15:50', '15:55', '16:00', '16:05', '16:10', '16:15', '16:20', '16:25', '16:30', '16:35', '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', '17:10', '17:15', '17:20', '17:25', '17:30', '17:35', '17:40', '17:45', '17:50', '17:55', '18:00', '18:05', '18:10', '18:15', '18:20', '18:25', '18:30', '18:35', '18:40', '18:45', '18:50', '18:55', '19:00', '19:05', '19:10', '19:15', '19:20', '19:25', '19:30', '19:35', '19:40', '19:45', '19:50', '19:55', '20:00', '20:05', '20:10', '20:15', '20:20', '20:25', '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00', '21:05', '21:10', '21:15', '21:20', '21:25', '21:30', '21:35', '21:40', '21:45', '21:50', '21:55', '22:00', '22:05', '22:10', '22:15', '22:20', '22:25', '22:30', '22:35', '22:40', '22:45', '22:50', '22:55', '23:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', '23:50', '23:55']
        for i in range((bb-aa).days+1):
            print(i ,"ayushJXHDKJHFKJDBH")
            query_results.append(CSV.objects.filter(date = aa+timedelta(days=i)).order_by('timestamp'))
            q = [str(aa+timedelta(days=i))]
            for x in query_results[i]:
                # print(x.load_value, x.timestamp, x.date)
                q.append(x.load_value)
            last.append(q)
            print(len(q))

            # single_query = []
            # for p in t[1:]:
            #     # single_query.append(CSV.objects.filter(date = aa+timedelta(days=i), timestamp=p))
            #     try:
            #         single_query.append(CSV.objects.filter(date = aa+timedelta(days=i), timestamp=p)[0].load_value)
            #     except Exception as e:
            #         single_query.append(None)
            #         baba = e
            # print(single_query)
            # single_query.insert(0,str(aa+timedelta(days=i)))
            # for x in single_query:
            #     q.append(x.load_value)
            # last.append(single_query)
            # print(query_results)
        # for x in query_results[0]:
        #     hour = x.timestamp.hour
        #     minutes = x.timestamp.minute
        #     t.append(str(hour)+':'+str(minutes))
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
        print("qqqqq")
        ans = qq.split('-')
        # bns = b.split('-')
        aa = datetime.date(int(ans[0]),int(ans[1]),int(ans[2]))
        # bb = datetime.date(int(bns[0]),int(bns[1]),int(bns[2])-p)
        query_results = []
        last = []
        l = []
        # t = ['x']
        for i in range(p+1):
            print(i ,"ayushJ")
            query_results.append((CSV.objects.filter(date = aa-timedelta(days=i)).order_by('timestamp')))
            q = [str(aa-timedelta(days=i))]
            for x in query_results[i]:
                q.append(x.load_value)
            last.append(q)
        # print(len(q))
        # print(last[1])
        # print(q)
        weights = [0.8019, 0.0426, 0.0226, -0.0169, 0.1497]
        weights_load = ['Forecasted with WMAVG']
        simple_load = ['Forecasted with SMAVG']
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
            weights_load.append(round((init1/total_weight), 2))
            simple_load.append(round((init/no_of_data),2))

        query_results1 = []
        last1_days = []
        no_day_alphamin = 30
        for i in range(no_day_alphamin):
            print(i ,"ayush")
            query_results1.append(CSV.objects.filter(date = aa-timedelta(days=(no_day_alphamin-i))))
            # q = [str(aa-timedelta(days=i))]
            loaddata = []
            for x in query_results1[i]:
                loaddata.append(x.load_value)
            last1_days.append(loaddata)
        alpha = [0]*288
        alphamin = [0]*288
        forecast_last1_days = [[0]*288 for i in range(no_day_alphamin)]

        forecast_last1_days[1] = last1_days[0][:]
        check_none=0
        while(len(last1_days[check_none]) != 288):
            check_none  = check_none + 1
            forecast_last1_days[check_none+1] = last1_days[check_none][:]
        for j in range(288):
            mse = [0]*9
            for k in range(1,10):
                alpha[j] = k*0.1
                for i in range(check_none+2,no_day_alphamin):
                    try:
                        forecast_last1_days[i][j] = (alpha[j]*last1_days[i-1][j]) + ((1 - alpha[j])*forecast_last1_days[i-1][j])
                    except Exception as e:
                        forecast_last1_days[i][j] = forecast_last1_days[i-1][j]
                for i in range(1+check_none,no_day_alphamin):
                    try:
                        mse[k-1] += (forecast_last1_days[i][j] - last1_days[i][j])**2
                    except Exception as e:
                        mse[k-1] += 0
            minimum = mse[0]
            alphamin[j] = 0.1
            for i in range(1,9):
                if mse[i]<minimum:
                    minimum = mse[i]
                    alphamin[j] = (i+1)*0.1
        forecasting = [[] for i in range(21)]
        forecasting[1] = last1_days[10][:]
        check_none1 = 0
        while(len(last1_days[10+check_none1]) != 288):
            check_none1 = check_none1+1
            forecasting[1+check_none1] = last1_days[10+check_none1][:]
        for j in range(2+check_none1,21):
            for i in range(288):
                try:
                    # print(i,j,last1_days[j+10-1][i])
                    forecasting[j].append(round(((alphamin[i]*last1_days[j+10-1][i]) + ((1 - alphamin[i])*forecasting[j-1][i])), 2))
                    # print(((alphamin[i]*last1_days[j+10-1][i]) + ((1 - alphamin[i])*forecasting[j-1][i])))
                except Exception as e:
                    # print(i,j)
                    forecasting[j].append(round(forecasting[j-1][i], 2))
                    # print((forecasting[j-1][i]))
        # print(".........",forecasting[20])
        forecasting[20].insert(0,"Forecasted with SES")



        # print(w)
        l.append(simple_load)
        l.append(weights_load)
        l.append(forecasting[20])
        l.append(last[0])
            # print(query_results)
        t = ['x', '00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30', '00:35', '00:40', '00:45', '00:50', '00:55', '01:00', '01:05', '01:10', '01:15', '01:20', '01:25', '01:30', '01:35', '01:40', '01:45', '01:50', '01:55', '02:00', '02:05', '02:10', '02:15', '02:20', '02:25', '02:30', '02:35', '02:40', '02:45', '02:50', '02:55', '03:00', '03:05', '03:10', '03:15', '03:20', '03:25', '03:30', '03:35', '03:40', '03:45', '03:50', '03:55', '04:00', '04:05', '04:10', '04:15', '04:20', '04:25', '04:30', '04:35', '04:40', '04:45', '04:50', '04:55', '05:00', '05:05', '05:10', '05:15', '05:20', '05:25', '05:30', '05:35', '05:40', '05:45', '05:50', '05:55', '06:00', '06:05', '06:10', '06:15', '06:20', '06:25', '06:30', '06:35', '06:40', '06:45', '06:50', '06:55', '07:00', '07:05', '07:10', '07:15', '07:20', '07:25', '07:30', '07:35', '07:40', '07:45', '07:50', '07:55', '08:00', '08:05', '08:10', '08:15', '08:20', '08:25', '08:30', '08:35', '08:40', '08:45', '08:50', '08:55', '09:00', '09:05', '09:10', '09:15', '09:20', '09:25', '09:30', '09:35', '09:40', '09:45', '09:50', '09:55', '10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45', '10:50', '10:55', '11:00', '11:05', '11:10', '11:15', '11:20', '11:25', '11:30', '11:35', '11:40', '11:45', '11:50', '11:55', '12:00', '12:05', '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45', '12:50', '12:55', '13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55', '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', '14:40', '14:45', '14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', '15:30', '15:35', '15:40', '15:45', '15:50', '15:55', '16:00', '16:05', '16:10', '16:15', '16:20', '16:25', '16:30', '16:35', '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', '17:10', '17:15', '17:20', '17:25', '17:30', '17:35', '17:40', '17:45', '17:50', '17:55', '18:00', '18:05', '18:10', '18:15', '18:20', '18:25', '18:30', '18:35', '18:40', '18:45', '18:50', '18:55', '19:00', '19:05', '19:10', '19:15', '19:20', '19:25', '19:30', '19:35', '19:40', '19:45', '19:50', '19:55', '20:00', '20:05', '20:10', '20:15', '20:20', '20:25', '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00', '21:05', '21:10', '21:15', '21:20', '21:25', '21:30', '21:35', '21:40', '21:45', '21:50', '21:55', '22:00', '22:05', '22:10', '22:15', '22:20', '22:25', '22:30', '22:35', '22:40', '22:45', '22:50', '22:55', '23:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', '23:50', '23:55']

        # for x in query_results[p]:
        #     hour = x.timestamp.hour
        #     minutes = x.timestamp.minute
        #     t.append(str(hour)+':'+str(minutes))
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
