#!/home/eee/ug/15084015/miniconda3/envs/TF/bin/python
from subprocess import call
import pdb
import pandas as pd
from datetime import datetime, timedelta


def scp(directory, date):
    cmd = ("scp -i /home/eee/ug/15084015/.ssh/btp.pem predictions/%s/%s.csv ubuntu@13.126.97.91:/var/www/html/btech_project/server/predictions/%s/" % (directory, date, directory))
    call(cmd.split(" "))

'''Simple Moving Average (SMA)'''
# pdb.set_trace()
p = 5  # number of days to take average of
n = 24*12  # hours * number of values per hour
time = ['00:00', '00:05', '00:10', '00:15', '00:20', '00:25', '00:30', '00:35', '00:40', '00:45', '00:50', '00:55', '01:00', '01:05', '01:10', '01:15', '01:20', '01:25', '01:30', '01:35', '01:40', '01:45', '01:50', '01:55', '02:00', '02:05', '02:10', '02:15', '02:20', '02:25', '02:30', '02:35', '02:40', '02:45', '02:50', '02:55', '03:00', '03:05', '03:10', '03:15', '03:20', '03:25', '03:30', '03:35', '03:40', '03:45', '03:50', '03:55', '04:00', '04:05', '04:10', '04:15', '04:20', '04:25', '04:30', '04:35', '04:40', '04:45', '04:50', '04:55', '05:00', '05:05', '05:10', '05:15', '05:20', '05:25', '05:30', '05:35', '05:40', '05:45', '05:50', '05:55', '06:00', '06:05', '06:10', '06:15', '06:20', '06:25', '06:30', '06:35', '06:40', '06:45', '06:50', '06:55', '07:00', '07:05', '07:10', '07:15', '07:20', '07:25', '07:30', '07:35', '07:40', '07:45', '07:50', '07:55', '08:00', '08:05', '08:10', '08:15', '08:20', '08:25', '08:30', '08:35', '08:40', '08:45', '08:50', '08:55', '09:00', '09:05', '09:10', '09:15', '09:20', '09:25', '09:30', '09:35', '09:40', '09:45', '09:50', '09:55', '10:00', '10:05', '10:10', '10:15', '10:20', '10:25', '10:30', '10:35', '10:40', '10:45', '10:50', '10:55', '11:00', '11:05', '11:10', '11:15', '11:20', '11:25', '11:30', '11:35', '11:40', '11:45', '11:50', '11:55',
        '12:00', '12:05', '12:10', '12:15', '12:20', '12:25', '12:30', '12:35', '12:40', '12:45', '12:50', '12:55', '13:00', '13:05', '13:10', '13:15', '13:20', '13:25', '13:30', '13:35', '13:40', '13:45', '13:50', '13:55', '14:00', '14:05', '14:10', '14:15', '14:20', '14:25', '14:30', '14:35', '14:40', '14:45', '14:50', '14:55', '15:00', '15:05', '15:10', '15:15', '15:20', '15:25', '15:30', '15:35', '15:40', '15:45', '15:50', '15:55', '16:00', '16:05', '16:10', '16:15', '16:20', '16:25', '16:30', '16:35', '16:40', '16:45', '16:50', '16:55', '17:00', '17:05', '17:10', '17:15', '17:20', '17:25', '17:30', '17:35', '17:40', '17:45', '17:50', '17:55', '18:00', '18:05', '18:10', '18:15', '18:20', '18:25', '18:30', '18:35', '18:40', '18:45', '18:50', '18:55', '19:00', '19:05', '19:10', '19:15', '19:20', '19:25', '19:30', '19:35', '19:40', '19:45', '19:50', '19:55', '20:00', '20:05', '20:10', '20:15', '20:20', '20:25', '20:30', '20:35', '20:40', '20:45', '20:50', '20:55', '21:00', '21:05', '21:10', '21:15', '21:20', '21:25', '21:30', '21:35', '21:40', '21:45', '21:50', '21:55', '22:00', '22:05', '22:10', '22:15', '22:20', '22:25', '22:30', '22:35', '22:40', '22:45', '22:50', '22:55', '23:00', '23:05', '23:10', '23:15', '23:20', '23:25', '23:30', '23:35', '23:40', '23:45', '23:50', '23:55']
data = pd.read_csv('monthdata.csv', header=None, index_col=['datetime'], names=[
                   'datetime', 'load'], parse_dates=['datetime'], infer_datetime_format=True)
today = datetime.strptime(
    data.index[-1].strftime("%d-%m-%Y %H:%M"), "%d-%m-%Y %H:%M") + timedelta(1)
date = today.strftime("%d-%m-%Y")
load = data['load'].values
pred = [0] * n
for i in range(n):
    forecast = 0
    for j in range(1, p+1):
        forecast += load[-(j * n)+i] / p
    pred[i] = (time[i], forecast)

df = pd.DataFrame.from_records(pred, columns=["time", "load"])
df.to_csv('predictions/SMA/%s.csv' % date, index=False)
scp('SMA', date)


'''Simple Exponential Smoothing (SES)'''
dict = {}

m = int(len(data)/n)
alpha = [0]*n
alphamin = [0]*n
forecast = [0]*len(data)
forecast[:n] = [load[j] for j in range(n)]

for j in range(n):
    mse = [0]*9
    for k in range(1, 10):
        alpha[j] = k*0.1
        mse[k-1] += (forecast[j] - load[n + j])**2
        for i in range(2, m):
            forecast[((i-1)*n) + j] = (alpha[j]*load[((i-1)*n) + j]
                                       ) + ((1 - alpha[j])*forecast[((i-2)*n) + j])
            mse[k-1] += (forecast[((i-1)*n) + j] - load[(i*n) + j])**2
    min = mse[0]
    alphamin[j] = 0.1
    for i in range(1, 9):
        if mse[i] < min:
            min = mse[i]
            alphamin[j] = (i+1)*0.1

a = 10
forecast2 = [0]*(a*n)
forecast2[:n] = [load[i-(a*n)] for i in range(n)]
for j in range(1, a):
    for i in range(n):
        forecast2[i+(j*n)] = (alphamin[i]*load[i-(a*n)+(j*n)]) + \
            ((1 - alphamin[i])*forecast2[i+(j*n)-n])
pred = [0]*n
for i in range(n):
    pred[i] = (time[i], forecast2[-n:][i])
labels = ["time", "load"]
df = pd.DataFrame.from_records(pred, columns=labels)
df.to_csv('predictions/SES/%s.csv' % date, index=False)
scp('SES', date)


'''Weighted Moving Average (WMA)'''
weights = [0.8019, 0.0426, 0.0226, -0.0169, 0.1497]
pred = [0] * n
for i in range(n):
    forecast = 0
    for j in range(1, len(weights)+1):
        forecast += load[-(j * n) + i] * weights[j-1]
    pred[i] = (time[i], forecast)

labels = ["time", "load"]
df = pd.DataFrame.from_records(pred, columns=labels)
df.to_csv('predictions/WMA/%s.csv' % date, index=False)
scp('WMA', date)
