#!/home/eee/ug/15084015/miniconda3/envs/btp/bin/python
"""The script is to run half an hour after midnight. Scrap last day's data and update lstm_data.csv"""
import os
import sys
from tensorflow import set_random_seed
from numpy.random import seed
from keras.layers import Dense, SimpleRNN, LSTM, GRU
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
import logging
from subprocess import call
from datetime import datetime, timedelta
import csv
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

seed(1)
set_random_seed(2)
# GPU is much slower due to small batch size, so use CPU only
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # no tf shit warnings


def get_load_data(date):
    url = "http://www.delhisldc.org/Loaddata.aspx?mode="
    logger.info("Scraping " + date)
    # send a get request to the url, get response
    resp = requests.get(url + date)
    soup = BeautifulSoup(resp.text, "lxml")  # Yummy HTML soup
    # get the table from html
    table = soup.find("table", {"id": "ContentPlaceHolder3_DGGridAv"})
    trs = table.findAll("tr")  # extract all rows of the table
    if len(trs[1:]) == 288:  # no need to create csv file, if there's no data
        # 'a' makes sure the values are appended at the end of the already existing file
        with open("lstm_data.csv", "a") as f:
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
        "lstm_data.csv",
        header=None,
        index_col=["datetime"],
        names=["datetime", "load"],
        parse_dates=["datetime"],
        infer_datetime_format=True,
    )


def prepare_data(data, nlags):
    """prepares data for LSTM model, x=last nlags values, y=(nlags+1)'th value"""
    data_x, data_y = [], []
    for i in range(data.shape[0]):
        for j in range(0, data.shape[1] - nlags):
            data_x.append(data[i, j : j + nlags])
            data_y.append(data[i, j + nlags])
    data_x = np.array(data_x)
    data_y = np.array(data_y).reshape(-1, 1)
    return data_x, data_y


def get_model(model_name):
    batch_size = 1
    if model_name == "RNN":
        model = Sequential()
        model.add(
            SimpleRNN(
                2,
                batch_input_shape=(batch_size, train_x.shape[1], train_x.shape[2]),
                stateful=True,
            )
        )
        model.add(Dense(train_y.shape[1]))
        model.compile(loss="mean_squared_error", optimizer="adam")
        return model

    elif model_name == "LSTM":
        model = Sequential()
        model.add(
            LSTM(
                1,
                batch_input_shape=(batch_size, train_x.shape[1], train_x.shape[2]),
                stateful=True,
            )
        )
        model.add(Dense(train_y.shape[1]))
        model.compile(loss="mean_squared_error", optimizer="adam")
        return model

    elif model_name == "GRU":
        model = Sequential()
        model.add(
            GRU(
                1,
                batch_input_shape=(batch_size, train_x.shape[1], train_x.shape[2]),
                stateful=True,
                return_sequences=True,
            )
        )
        model.add(GRU(1, stateful=True))
        model.add(Dense(train_y.shape[1]))
        model.compile(loss="mean_squared_error", optimizer="adam")
        return model


# to store the log in a file called 'arima_log.txt'
logging.basicConfig(
    filename="aws_rnn_log.txt",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)
logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)
sys.stdout = open('aws_rnn_log.txt', 'a')


"""Check if lstm_data.csv exists, if no then create one, if yes then update it 
with yesterday's data and clip it so that it contains only last 60 days of data,
as the model is to be trained on last 60 days of data."""
if os.path.exists("lstm_data.csv"):
    data = get_data()
    # yesterdays data not present, scrap it
    if (datetime.today() - timedelta(1)).date().strftime('%Y-%m-%d') == str(data.index.date[-1]):
        # only need to scrap for yesterday's data and append it to already existing file
        yesterday = datetime.today() - timedelta(1)
        yesterday = yesterday.strftime("%d/%m/%Y")
        get_load_data(yesterday)
        # re read updated lstm_data.csv and clip data in lstm_data.csv to last 60 days only
        data = get_data()
        day_to_clip_from = datetime.today() - timedelta(61)
        logger.info("Clipping data from " + day_to_clip_from.strftime("%d/%m/%Y"))
        data = data[day_to_clip_from.strftime("%d/%m/%Y") :]
        # IMP: don't add any header to the lstm_data.csv
        data.to_csv("lstm_data.csv", header=False)
    else:
        logger.info('Yesterday"s load already scrapped!')
else:  # scrap for last 60 days, prepare lstm_data.csv
    print("Creating lstm_data.csv ..")
    for i in range(61, 0, -1):
        yesterday = datetime.today() - timedelta(i)
        yesterday = yesterday.strftime("%d/%m/%Y")
        get_load_data(yesterday)
    data = get_data()


logger.info(data.shape)

data = pd.read_csv(
    "lstm_data.csv",
    header=None,
    names=["datetime", "load"],
    index_col=[0],
    parse_dates=[0],
    infer_datetime_format=True,
)
df = pd.DataFrame(columns=["time"] + list(map(str, range(int(data.shape[0] / 288)))))
for idx, time in enumerate(sorted(set(data.index.time))):
    df.loc[idx] = [time.strftime(format="%H:%M:%S")] + list(
        data.at_time(time)["load"].values
    )
df.index = df["time"]
df = df.drop("time", 1)
dt_df = df.diff(1, axis=1)  # detrending
dt_df = dt_df.dropna(axis=1)  # droping the na column created due to detrending
scaler = MinMaxScaler(feature_range=(-1, 1))  # rescaling data to [-1, 1]
scaler = scaler.fit(dt_df.values.reshape(-1, 1))
dt_df = scaler.transform(dt_df)  # dt_df is now a numpy array
split_idx = int(len(dt_df) * 0.8)
train, val = dt_df[:split_idx, :], dt_df[split_idx:, :]

nlags = 10  # number of previous days to use for prediction
batch_size = 1  # batch size to train the models on
train_x, train_y = prepare_data(train, nlags)
val_x, val_y = prepare_data(val, nlags)
train_x = train_x.reshape(train_x.shape[0], 1, nlags)
val_x = val_x.reshape(val_x.shape[0], 1, nlags)

# data for prediction of today's load
# slice last nlags+1 days from df, will be used in prediction of yesterday's data
df_last_nlags_plus_one = df.loc[:, df.columns[-nlags - 1:]]
# taking last 21 days, differencing and dropping the nan value
dt_df_last_nlags = df_last_nlags_plus_one.diff(1, axis=1).dropna(axis=1)
dt_df_last_nlags = scaler.transform(dt_df_last_nlags)  # df is now a numpy array
X = dt_df_last_nlags.reshape(dt_df_last_nlags.shape[0], 1, nlags)  # nlags=20
today = datetime.today().strftime(format="%d-%m-%Y")
models = ["LSTM", "RNN", "GRU"]

for model_name in models:
    logger.info("%s training started" % model_name)
    model = get_model(model_name)
    logger.info(model.summary())
    print(model.summary())
    for i in range(15):
        history = model.fit(
            train_x,
            train_y,
            epochs=1,
            batch_size=batch_size,
            verbose=2,
            validation_data=(val_x, val_y),
            shuffle=False,
        )
        model.reset_states()

    # calculate val RMSE
    val_y_pred = model.predict(val_x, batch_size=batch_size, verbose=2)
    inverted_val_y = scaler.inverse_transform(val_y)
    inverted_val_y_pred = scaler.inverse_transform(val_y_pred)
    val_RMSE = np.sqrt(
        np.sum(np.square(np.array(inverted_val_y_pred) - np.array(inverted_val_y)))
        / len(inverted_val_y)
    )
    logger.info("model name: %s  |  val_RMSE: %f" % (model_name, val_RMSE))
    # import pdb; pdb.set_trace()
    # Predict today's load
    Y = model.predict(X, batch_size=batch_size)  # predict for today's values
    inv_Y = scaler.inverse_transform(Y)  # invert to detrended values' scale
    # last day's values added to inv_Y to get it to original scale
    rescaled_Y = [x + y for x, y in zip(inv_Y[:, 0], df.iloc[:, -1])]

    # create a csv file to store the predictions
    pred_df = pd.DataFrame(columns=["time", "load"])
    pred_df["time"] = list(df.index)
    pred_df["load"] = rescaled_Y
    pred_df.to_csv("predictions/%s/%s.csv" % (model_name, today), index=False)
    # now, send the file to the AWS server using scp
    cmd = (
        "scp -i /home/eee/ug/15084015/.ssh/btp.pem predictions/%s/%s.csv ubuntu@13.126.97.91:/var/www/html/btech_project/server/predictions/%s/"
        % (model_name, today, model_name)
    )
    logger.info(call(cmd.split(" ")))
