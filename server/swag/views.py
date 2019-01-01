from django.shortcuts import render, HttpResponse
from django.utils.safestring import mark_safe
import datetime
from datetime import timedelta
import json
import requests
import csv
import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from .models import CSV


def home_page(request):
    print("date:", datetime.date.today().day)
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    return render(request, "Home_page.html", {'Day': str(day).zfill(2),
                                        'Month': str(month).zfill(2),
                                        'Year': year})


def graph_plot(request):
    if request.method == 'POST':
        # print(request.POST)
        a = request.POST['from']
        b = request.POST['to']
        ans = a.split('-')
        bns = b.split('-')
        aa = datetime.date(int(ans[0]),int(ans[1]),int(ans[2]))
        bb = datetime.date(int(bns[0]),int(bns[1]),int(bns[2]))
        query_results = []
        last = []
        t = ['x', '00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30', '00:35', '00:40', '00:45', '00:50', '00:55', '01:00', '01:05', '01:10', '01:15', '01:20', '01:25', '01:30', '01:35', '01:40', '01:45', '01:50', '01:55', '02:00', '02:05', '02:10', '02:15', '02:20', '02:25', '02:30', '02:35', '02:40', '02:45', '02:50', '02:55', '03:00', '03:05', '03:10', '03:15', '03:20', '03:25', '03:30', '03:35', '03:40', '03:45', '03:50', '03:55', '04:00', '04:05', '04:10', '04:15', '04:20', '04:25', '04:30', '04:35', '04:40', '04:45', '04:50', '04:55', '05:00', '05:05', '05:10', '05:15', '05:20', '05:25', '05:30', '05:35', '05:40', '05:45', '05:50', '05:55', '06:00', '06:05', '06:10', '06:15', '06:20', '06:25', '06:30', '06:35', '06:40', '06:45', '06:50', '06:55', '07:00', '07:05', '07:10', '07:15', '07:20', '07:25', '07:30', '07:35', '07:40', '07:45', '07:50', '07:55', '08:00', '08:05', '08:10', '08:15', '08:20', '08:25', '08:30', '08:35', '08:40', '08:45', '08:50', '08:55', '09:00', '09:05', '09:10', '09:15', '09:20', '09:25', '09:30', '09:35', '09:40', '09:45', '09:50', '09:55', '10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45', '10:50', '10:55', '11:00', '11:05', '11:10', '11:15', '11:20', '11:25', '11:30', '11:35', '11:40', '11:45', '11:50', '11:55', '12:00', '12:05', '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45', '12:50', '12:55', '13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55', '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', '14:40', '14:45', '14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', '15:30', '15:35', '15:40', '15:45', '15:50', '15:55', '16:00', '16:05', '16:10', '16:15', '16:20', '16:25', '16:30', '16:35', '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', '17:10', '17:15', '17:20', '17:25', '17:30', '17:35', '17:40', '17:45', '17:50', '17:55', '18:00', '18:05', '18:10', '18:15', '18:20', '18:25', '18:30', '18:35', '18:40', '18:45', '18:50', '18:55', '19:00', '19:05', '19:10', '19:15', '19:20', '19:25', '19:30', '19:35', '19:40', '19:45', '19:50', '19:55', '20:00', '20:05', '20:10', '20:15', '20:20', '20:25', '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00', '21:05', '21:10', '21:15', '21:20', '21:25', '21:30', '21:35', '21:40', '21:45', '21:50', '21:55', '22:00', '22:05', '22:10', '22:15', '22:20', '22:25', '22:30', '22:35', '22:40', '22:45', '22:50', '22:55', '23:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', '23:50', '23:55']
        for i in range((bb-aa).days+1):
            query_results.append(CSV.objects.filter(date = aa+timedelta(days=i)).order_by('timestamp'))
            q = [str(aa+timedelta(days=i))]
            for x in query_results[i]:
                q.append(x.load_value)
            last.append(q)

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
    if request.method == 'POST':
        qq = request.POST['fc']
        ans = qq.split('-')
        aa = datetime.date(int(ans[0]),int(ans[1]),int(ans[2]))
        day = aa.day
        month = aa.month
        year = aa.year
        query_results = []
        l = []
        query_results.append((CSV.objects.filter(date = aa).order_by('timestamp')))
        q = [str(aa)]
        for x in query_results[0]:
            q.append(x.load_value)

        # weights = [0.8019, 0.0426, 0.0226, -0.0169, 0.1497]
        ARIMA_load = ['Forecasted with ARIMA']
        WMA_load = ['Forecasted with WMA']
        SMA_load = ['Forecasted with SMA']
        LSTM_load = ['Forecasted with LSTM']
        SES_load = ['Forecasted with SES']
        GRU_load = ['Forecasted with GRU']
        RNN_load = ['Forecasted with RNN']

        csv_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(str(day).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+'.csv')

        arima_csv = pd.read_csv(os.path.join(csv_path, 'predictions/ARIMA/'+str(day).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+'.csv'))['load'].values
        ARIMA_load.extend(list(arima_csv))
        wma_csv = pd.read_csv(os.path.join(csv_path, 'predictions/WMA/'+str(day).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+'.csv'))['load'].values
        WMA_load.extend(list(wma_csv))

        sma_csv = pd.read_csv(os.path.join(csv_path, 'predictions/SMA/'+str(day).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+'.csv'))['load'].values
        SMA_load.extend(list(sma_csv))

        ses_csv = pd.read_csv(os.path.join(csv_path, 'predictions/SES/'+str(day).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+'.csv'))['load'].values
        SES_load.extend(list(ses_csv))

        lstm_csv = pd.read_csv(os.path.join(csv_path, 'predictions/LSTM/'+str(day).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+'.csv'))['load'].values
        LSTM_load.extend(list(lstm_csv))

        gru_csv = pd.read_csv(os.path.join(csv_path, 'predictions/GRU/'+str(day).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+'.csv'))['load'].values
        GRU_load.extend(list(gru_csv))

        rnn_csv = pd.read_csv(os.path.join(csv_path, 'predictions/RNN/'+str(day).zfill(2)+"-"+str(month).zfill(2)+"-"+str(year)+'.csv'))['load'].values
        RNN_load.extend(list(rnn_csv))

        l.append(SMA_load)
        l.append(WMA_load)
        l.append(SES_load)
        l.append(ARIMA_load)
        l.append(LSTM_load)
        l.append(GRU_load)
        l.append(RNN_load)
        l.append(q)        #q==actual
        redu = q.count(None)
        length = len(q)-redu
        t = ['x', '00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30', '00:35', '00:40', '00:45', '00:50', '00:55', '01:00', '01:05', '01:10', '01:15', '01:20', '01:25', '01:30', '01:35', '01:40', '01:45', '01:50', '01:55', '02:00', '02:05', '02:10', '02:15', '02:20', '02:25', '02:30', '02:35', '02:40', '02:45', '02:50', '02:55', '03:00', '03:05', '03:10', '03:15', '03:20', '03:25', '03:30', '03:35', '03:40', '03:45', '03:50', '03:55', '04:00', '04:05', '04:10', '04:15', '04:20', '04:25', '04:30', '04:35', '04:40', '04:45', '04:50', '04:55', '05:00', '05:05', '05:10', '05:15', '05:20', '05:25', '05:30', '05:35', '05:40', '05:45', '05:50', '05:55', '06:00', '06:05', '06:10', '06:15', '06:20', '06:25', '06:30', '06:35', '06:40', '06:45', '06:50', '06:55', '07:00', '07:05', '07:10', '07:15', '07:20', '07:25', '07:30', '07:35', '07:40', '07:45', '07:50', '07:55', '08:00', '08:05', '08:10', '08:15', '08:20', '08:25', '08:30', '08:35', '08:40', '08:45', '08:50', '08:55', '09:00', '09:05', '09:10', '09:15', '09:20', '09:25', '09:30', '09:35', '09:40', '09:45', '09:50', '09:55', '10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45', '10:50', '10:55', '11:00', '11:05', '11:10', '11:15', '11:20', '11:25', '11:30', '11:35', '11:40', '11:45', '11:50', '11:55', '12:00', '12:05', '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45', '12:50', '12:55', '13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55', '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', '14:40', '14:45', '14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', '15:30', '15:35', '15:40', '15:45', '15:50', '15:55', '16:00', '16:05', '16:10', '16:15', '16:20', '16:25', '16:30', '16:35', '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', '17:10', '17:15', '17:20', '17:25', '17:30', '17:35', '17:40', '17:45', '17:50', '17:55', '18:00', '18:05', '18:10', '18:15', '18:20', '18:25', '18:30', '18:35', '18:40', '18:45', '18:50', '18:55', '19:00', '19:05', '19:10', '19:15', '19:20', '19:25', '19:30', '19:35', '19:40', '19:45', '19:50', '19:55', '20:00', '20:05', '20:10', '20:15', '20:20', '20:25', '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00', '21:05', '21:10', '21:15', '21:20', '21:25', '21:30', '21:35', '21:40', '21:45', '21:50', '21:55', '22:00', '22:05', '22:10', '22:15', '22:20', '22:25', '22:30', '22:35', '22:40', '22:45', '22:50', '22:55', '23:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', '23:50', '23:55']
        l.insert(0, t)
    else:
        l = None
    print(l)

    def mean_absolute_percentage_error(y_pred, y_true):
        print('mape:', y_pred, y_true)
        try:
            y_true, y_pred = np.array(y_true), np.array(y_pred)
            mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        except Exception as e:
            mape = e
        return mape

    def root_mean_square_error(y_pred, y_true):
        print('rmse:', y_pred, y_true)
        try:
            y_true, y_pred = np.array(y_true), np.array(y_pred)
            rmse = np.sqrt((y_pred - y_true)**2).mean()
        except Exception as e:
            rmse = e
        return rmse


    cont = {
            # "query_results":query_results,
            'forecasted_Load': l,
            'rmseSMA': round(root_mean_square_error(l[1][1:length], l[8][1:length]), 2),
            'rmseWMA': round(root_mean_square_error(l[2][1:length], l[8][1:length]), 2),
            'rmseSES': round(root_mean_square_error(l[3][1:length], l[8][1:length]), 2),
            'rmseARIMA': round(root_mean_square_error(l[4][1:length], l[8][1:length]), 2),
            'rmseLSTM': round(root_mean_square_error(l[5][1:length], l[8][1:length]), 2),
            'rmseGRU': round(root_mean_square_error(l[6][1:length], l[8][1:length]), 2),
            'rmseRNN': round(root_mean_square_error(l[7][1:length], l[8][1:length]), 2),

            'mapeSMA': round(mean_absolute_percentage_error(l[1][1:length], l[8][1:length]),2),
            'mapeWMA': round(mean_absolute_percentage_error(l[2][1:length], l[8][1:length]),2),
            'mapeSES': round(mean_absolute_percentage_error(l[3][1:length], l[8][1:length]),2),
            'mapeARIMA': round(mean_absolute_percentage_error(l[4][1:length], l[8][1:length]),2),
            'mapeLSTM': round(mean_absolute_percentage_error(l[5][1:length], l[8][1:length]),2),
            'mapeGRU': round(mean_absolute_percentage_error(l[6][1:length], l[8][1:length]),2),
            'mapeRNN': round(mean_absolute_percentage_error(l[7][1:length], l[8][1:length]),2),

            # 'Tarikh':a,
            # 'T':mark_safe(t),
            # 'Load': [x.load_value for x in query_results],
            # 'Time': [x.timestamp for x in query_results],
        }
    # print(cont)
    return HttpResponse(json.dumps(cont),content_type='application/json')
