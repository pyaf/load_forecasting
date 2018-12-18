#!/home/eee/ug/15084015/miniconda3/envs/btp/bin/python
from subprocess import call
import pdb
import pandas as pd
from datetime import datetime, timedelta


def scp(directory, date):
    cmd = (
        "scp -i /home/eee/ug/15084015/.ssh/btp.pem predictions/%s/%s.csv ubuntu@13.126.97.91:/var/www/html/btech_project/server/predictions/%s/"
        % (directory, date, directory)
    )
    call(cmd.split(" "))


"""Simple Moving Average (SMA)"""
# pdb.set_trace()
p = 5  # number of days to take average of
n = 24 * 12  # hours * number of values per hour
time = ['%02d:%02d' % (x, y) for x in range(24) for y in range(0, 60, 5)]
#time = ['00:00', '00:05'...

data = pd.read_csv(
    "monthdata.csv",
    header=None,
    index_col=["datetime"],
    names=["datetime", "load"],
    parse_dates=["datetime"],
    infer_datetime_format=True,
)
# import pdb; pdb.set_trace()
print(data.index[-1])
date = datetime.today().date().strftime("%d-%m-%Y")
print('date today:', date)
load = data["load"].values
pred = [0] * n
for i in range(n):
    forecast = 0
    for j in range(1, p + 1):
        forecast += load[-(j * n) + i] / p
    pred[i] = (time[i], forecast)

df = pd.DataFrame.from_records(pred, columns=["time", "load"])
df.to_csv("predictions/SMA/%s.csv" % date, index=False)
scp("SMA", date)


"""Simple Exponential Smoothing (SES)"""
dict = {}

m = int(len(data) / n)
alpha = [0] * n
alphamin = [0] * n
forecast = [0] * len(data)
forecast[:n] = [load[j] for j in range(n)]

for j in range(n):
    mse = [0] * 9
    for k in range(1, 10):
        alpha[j] = k * 0.1
        mse[k - 1] += (forecast[j] - load[n + j]) ** 2
        for i in range(2, m):
            forecast[((i - 1) * n) + j] = (alpha[j] * load[((i - 1) * n) + j]) + (
                (1 - alpha[j]) * forecast[((i - 2) * n) + j]
            )
            mse[k - 1] += (forecast[((i - 1) * n) + j] - load[(i * n) + j]) ** 2
    min = mse[0]
    alphamin[j] = 0.1
    for i in range(1, 9):
        if mse[i] < min:
            min = mse[i]
            alphamin[j] = (i + 1) * 0.1

a = 10
forecast2 = [0] * (a * n)
forecast2[:n] = [load[i - (a * n)] for i in range(n)]
for j in range(1, a):
    for i in range(n):
        forecast2[i + (j * n)] = (alphamin[i] * load[i - (a * n) + (j * n)]) + (
            (1 - alphamin[i]) * forecast2[i + (j * n) - n]
        )
pred = [0] * n
for i in range(n):
    pred[i] = (time[i], forecast2[-n:][i])
labels = ["time", "load"]
df = pd.DataFrame.from_records(pred, columns=labels)
df.to_csv("predictions/SES/%s.csv" % date, index=False)
scp("SES", date)


"""Weighted Moving Average (WMA)"""
weights = [0.8019, 0.0426, 0.0226, -0.0169, 0.1497]
pred = [0] * n
for i in range(n):
    forecast = 0
    for j in range(1, len(weights) + 1):
        forecast += load[-(j * n) + i] * weights[j - 1]
    pred[i] = (time[i], forecast)

labels = ["time", "load"]
df = pd.DataFrame.from_records(pred, columns=labels)
df.to_csv("predictions/WMA/%s.csv" % date, index=False)
scp("WMA", date)
