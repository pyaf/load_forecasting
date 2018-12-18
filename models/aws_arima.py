#!/home/eee/ug/15084015/miniconda3/envs/btp/bin/python
"""
The script is to run half an hour after midnight. Scrap last day's data and update monthsdata.csv
"""
import os
import logging
from math import sqrt
from subprocess import call
from datetime import datetime, timedelta
import csv
import requests
import numpy as np
import pandas as pd
import statsmodels.api as sm
from bs4 import BeautifulSoup
from statsmodels.tsa.arima_model import ARIMAResults


def get_load_data(date):
    url = "http://www.delhisldc.org/Loaddata.aspx?mode="
    logger.info("Scraping " + date)
    resp = requests.get(url + date)  # send a get request to the url, get response
    soup = BeautifulSoup(resp.text, "lxml")  # Yummy HTML soup
    table = soup.find(
        "table", {"id": "ContentPlaceHolder3_DGGridAv"}
    )  # get the table from html
    trs = table.findAll("tr")  # extract all rows of the table
    if len(trs[1:]) == 288:  # no need to create csv file, if there's no data
        with open(
            "monthdata.csv", "a"
        ) as f:  #'a' makes sure the values are appended at the end of the already existing file
            writer = csv.writer(f)
            for tr in trs[1:]:
                time, delhi = tr.findChildren("font")[:2]
                writer.writerow([date + " " + time.text, delhi.text])
    if len(trs[1:]) != 288:
        logger.info("Some of the load values are missing..")
    else:
        logger.info("Done")


def get_data():
    return pd.read_csv(
        "monthdata.csv",
        header=None,
        index_col=["datetime"],
        names=["datetime", "load"],
        parse_dates=["datetime"],
        infer_datetime_format=True,
    )


# to store the log in a file called 'arima_log.txt'
logging.basicConfig(
    filename="aws_arima_log.txt",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)
logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)

"""Check if monthdata.csv exists, if no then create one, if yes then update it with yesterday's data and clip it so that it contains only last 30 days of data,
as the model is to be trained on last 30 days of data."""
if os.path.exists("monthdata.csv"):
    data = get_data()
    # import pdb; pdb.set_trace()
    if (datetime.today() - timedelta(1)).date().strftime('%Y-%m-%d') != str(data.index.date[-1]):  # yesterdays data not present, scrap it
        # only need to scrap for yesterday's data and append it to already existing file
        yesterday = datetime.today() - timedelta(1)
        yesterday = yesterday.strftime("%d/%m/%Y")
        get_load_data(yesterday)
        # re read updated monthdata.csv and clip data in monthdata.csv to last 30 days only
        data = get_data()
        day_to_clip_from = datetime.today() - timedelta(30)
        logger.info("Clipping data from " + day_to_clip_from.strftime("%d/%m/%Y"))
        data = data[day_to_clip_from.strftime("%d/%m/%Y"):]
        data.to_csv(
            "monthdata.csv", header=False
        )  # IMP: don't add any header to the monthdata.csv
    else:
        logger.info('Yesterday"s load already scrapped!')
else:  # scrap for last 30 days, prepare monthdata.csv
    for i in range(31, 0, -1):
        yesterday = datetime.today() - timedelta(i)
        yesterday = yesterday.strftime("%d/%m/%Y")
        get_load_data(yesterday)
    data = get_data()

# exit()
logger.info(data.shape)
data = data.asfreq(freq="30Min", method="bfill")  # sample the data in hourly manner

# initialize the model
model = sm.tsa.statespace.SARIMAX(
    data,
    order=(3, 1, 1),
    seasonal_order=(3, 0, 0, 24),
    enforce_stationarity=False,
    enforce_invertibility=False,
)

# fit the model with the data
logger.info("Starting model fitting...")
model = model.fit()

logger.info("Model fitting done!!")
logger.info(model.summary().tables[1])
logger.info(model.summary())

# save the model
model.save("ARIMA_month_model.pkl")
# model = ARIMAResults.load('ARIMA_month_model.pkl')
# import pdb; pdb.set_trace()
# generate the predictions
todays_date = datetime.today().strftime("%d/%m/%Y")
tommorows_date = (datetime.today() + timedelta(1)).strftime("%d/%m/%Y")
# pred = model.get_prediction(
#     start=data.shape[0]-9,  # rolling mean of window 10 to be applied
#     end=data.shape[0]+48-1,  # predict next 48 values (half hourly, for 24 hours), last value to be removed 
#     dynamic=False,
# )
pred = model.get_prediction(
    start=data.shape[0],  # rolling mean of window 10 to be applied
    end=data.shape[0]+48,  # predict next 48 values (half hourly, for 24 hours), last value to be removed 
    dynamic=False,
)
# save the pridictions in a csv file
predictions = pred.predicted_mean
predictions = predictions.asfreq(freq="5Min", method="bfill")  # set to 5 min freq
date = datetime.today().strftime(format="%d-%m-%Y")
# predictions = predictions.rolling(window=10).mean().dropna()
predictions.to_csv(
    "predictions/ARIMA/%s.csv" % date, index_label="datetime", header=["load"]
)

# error = sqrt(((predictions - numpy.squeeze(todays_date['%s' % date:]))**2).mean())
# logger.log(error)

# now, send the file to the AWS server using scp
cmd = (
    "scp -i /home/eee/ug/15084015/.ssh/btp.pem predictions/ARIMA/%s.csv ubuntu@13.126.97.91:/var/www/html/btech_project/server/predictions/ARIMA/"
    % (date)
)
logger.info(call(cmd.split(" ")))
print("ARIMA prediction done")
