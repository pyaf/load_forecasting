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


# to store the log in a file called 'arima_log.txt'
logging.basicConfig(
    filename='arima_log.txt',
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)
logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)


def get_load_data(date):
    url = 'http://www.delhisldc.org/Loaddata.aspx?mode='
    logger.info('Scraping', date)
    resp = requests.get(url+date) # send a get request to the url, get response
    soup = BeautifulSoup(resp.text, 'lxml') # Yummy HTML soup
    table = soup.find('table', {'id':'ContentPlaceHolder3_DGGridAv'}) # get the table from html
    trs = table.findAll('tr') # extract all rows of the table
    if len(trs[1:])!=0: # no need to create csv file, if there's no data, for Aug month of 2017
        csv_filename = 'monthdata.csv'
        with open(csv_filename, 'a') as f:  #'a' makes sure the values are appended at the end of the already existing file
            writer = csv.writer(f)
            count=0
            for tr in trs[1:]:
                time, delhi = tr.findChildren('font')[:2]
                writer.writerow([date+' '+time.text, delhi.text])
                count+=1
    if count != 288:
        logger.info('Some of the load values are missing..')
    else:
        logger.info('Done')


# if os.path.exists('monthdata.csv'):
#     # only need to scrap for yesterday's data and append it to already existing file
#     yesterday = datetime.today() - timedelta(1)
#     yesterday = yesterday.strftime('%d/%m/%Y')
#     get_load_data(yesterday)    
# else:  # scrap for last 30 days, prepare monthdata.csv
#     for i in range(31, 0, -1):
#         yesterday = datetime.today() - timedelta(i)
#         yesterday = yesterday.strftime('%d/%m/%Y')
#         get_load_data(yesterday)    

# load the month long data
data = pd.read_csv('monthdata.csv', header=None, names=['datetime', 'load'], index_col=[0], parse_dates=[0], infer_datetime_format=True)

# clip data and monthdata.csv to last 30 days only
day_to_clip_from = datetime.today() - timedelta(30)
data = data[day_to_clip_from.strftime('%d/%m/%Y'):]
data.to_csv('monthdata.csv', columns=None)

logger.info(data.head())
data = data.asfreq(freq='0.4H', method='bfill')  # sample the data in hourly manner

# initialize the model
model = sm.tsa.statespace.SARIMAX(data,
                                order=(0,1,1),
                                seasonal_order=(0,2,2,24),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

# fit the model with the data
logger.info('Starting model fitting...')
model = model.fit()

logger.info('Model fitting done!!')
logger.info(results.summary().tables[1])
logger.info(results.summary())

# save the model
model.save('ARIMA_month_model.pkl')

# generate the predictions
todays_date = datetime.today().strftime('%d/%m/%Y')
pred = model.get_prediction(start=pd.to_datetime('%s 00:00:00' % todays_date), end=pd.to_datetime('%s 23:00:00' % todays_date), dynamic=False)

# save the pridictions in a csv file
predictions = pred.predicted_mean
predictions = predictions.asfreq(freq='5Min', method='bfill')  # set to 5 min freq
predictions.to_csv('arima_pred.csv', index_label='datetime', header=['load'])

# error = sqrt(((predictions - numpy.squeeze(todays_date['%s' % date:]))**2).mean())
# logger.log(error)

# now, send the file to the AWS server using scp
cmd = "scp -i /home/eee/ug/15084015/.ssh/btp.pem arima_pred.csv ubuntu@13.126.97.91:/var/www/html/btech_project/server/static/"
logger.info(call(cmd.split(" ")))