
# coding: utf-8

# In[38]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import statsmodels.api as sm
from statsmodels.tsa import stattools
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf
import os
import logging
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas import datetime
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
os.environ['CUDA_VISIBLE_DEVICES']=''

import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.4
sess = tf.Session(config=config)

from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from keras.layers import LSTM
from math import sqrt
from matplotlib import pyplot
from numpy import array
from sklearn.preprocessing import MinMaxScaler



np.random.seed(1)
tf.set_random_seed(2)

print('imported')
# to store the log in a file called 'arima_log.txt'
logging.basicConfig(
    filename='LSTM_v2_log.txt',
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)
logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)


logger.info("Preparing data...")
data = pd.read_csv('lstm_data.csv', header=None, names=['datetime', 'load'], index_col=[0], parse_dates=[0], infer_datetime_format=True)

df = pd.DataFrame(columns=['time'] + list(map(str, range(int(data.shape[0] / 288)))))

# In[11]:


for idx, time in enumerate(sorted(set(data.index.time))):
    df.loc[idx] = [time.strftime(format='%H:%M:%S')] + list(data.at_time(time)['load'].values)
#     data.at_time(time).plot()


df.index = df['time']
df = df.drop('time', 1)


dt_df = df.diff(1, axis=1)

dt_df = dt_df.dropna(axis=1)

scaler = MinMaxScaler(feature_range=(-1, 1))
scaler = scaler.fit(dt_df.values.reshape(-1, 1))

dt_df = scaler.transform(dt_df)  # dt_df is now a numpy array

split_idx = int(len(dt_df) * 0.8)
train, val = dt_df[:split_idx, :], dt_df[split_idx:, :]


def prepare_data(data, nlags):
    '''prepares data for LSTM model, x=last nlags values, y=(nlags+1)'th value'''
    data_x, data_y = [], []
    for i in range(data.shape[0]):
        for j in range(0, data.shape[1]-nlags):
            data_x.append(data[i, j:j+nlags])
            data_y.append(data[i, j+nlags])
    data_x = np.array(data_x)
    data_y = np.array(data_y).reshape(-1, 1)
    return data_x, data_y


nlags = 10
train_x, train_y = prepare_data(train, nlags)
val_x, val_y = prepare_data(val, nlags)


train_x = train_x.reshape(train_x.shape[0], 1, nlags)
val_x = val_x.reshape(val_x.shape[0], 1, nlags)

df_last_nlags_plus_one = df.loc[:, df.columns[-nlags-1:]]  # slice last nlags+1 days from df, will be used in prediction of yesterday's data
dt_df_last_nlags = df_last_nlags_plus_one.diff(1, axis=1).dropna(axis=1)  #taking last 21 days, differencing and dropping the nan value
dt_df_last_nlags = scaler.transform(dt_df_last_nlags)  # df is now a numpy array
X = dt_df_last_nlags.reshape(dt_df_last_nlags.shape[0], 1, nlags)  # nlags=20
load = np.load('25nov.npy')

logger.info('Data prepared. Starting grid search')

for node_num in range(1, 20):
    model = Sequential()
    model.add(LSTM(node_num, batch_input_shape=(1, train_x.shape[1], train_x.shape[2]), stateful=True))
    model.add(Dense(train_y.shape[1]))
    model.compile(loss='mean_squared_error', optimizer='adam')
    early_stopping_counter = 0
    last_loss = np.inf
    for i in range(20):
        history = model.fit(train_x, train_y, epochs=1, batch_size=1, verbose=0, validation_data=(val_x, val_y), shuffle=False)
        model.reset_states()
        val_loss = history.history['val_loss'][0]
        if val_loss > last_loss:
            early_stopping_counter += 1
        else:    
            early_stopping_counter = 0
        last_loss = val_loss
        if early_stopping_counter == 2:
            break

    val_y_pred = model.predict(val_x, batch_size=1)
    inverted_val_y = scaler.inverse_transform(val_y)
    inverted_val_y_pred = scaler.inverse_transform(val_y_pred)
    val_RMSE = np.sqrt(np.sum(np.square(np.array(inverted_val_y_pred) - np.array(inverted_val_y))) / len(inverted_val_y)) 


    Y = model.predict(X, batch_size=1)  # predict for today's values
    inv_Y = scaler.inverse_transform(Y)  # invert to detrended values' scale
    rescaled_Y = [x+y for x, y in zip(inv_Y[:, 0], df.iloc[:, -1])]  # last day's values added to inv_Y to get it to original scale
    nov_24_RMSE = np.sqrt(np.sum(np.square(np.array(rescaled_Y) - load)) / len(load)) 
    del model
    logger.info("num of neurons in first LSTM layer: %d , nov_24_RMSE: %f , val_RMSE: %f" % (node_num, nov_24_RMSE, val_RMSE))




