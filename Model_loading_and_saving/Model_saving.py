import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa import stattools
from math import sqrt

delhi = pd.read_csv('delhi.csv', header = None, parse_dates=[[0,1]], infer_datetime_format=True)
delhi.columns = ['datetime', 'load']
delhi.index = delhi['datetime']
delhi = delhi.drop(columns = ['datetime'])
delhi = delhi.asfreq(freq='30T', method='bfill')
delhi = delhi['2018':]
mod = sm.tsa.statespace.SARIMAX(delhi,
                                order=(1,1,1),
                                seasonal_order=(1,1,1,48),# 48 is seasonal period of the given data
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
results.save('29_model.pkl') # create pkl file to store model