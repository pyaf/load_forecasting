# Models

Models implemented during the course of the project:

* Feed forward Neural Network [FFNN.ipynb](FFNN.ipynb)
* Simple Moving Average [SMA.ipynb](SMA.ipynb)
* Weighted Moving Average [WMA.ipynb](WMA.ipynb)
* Simple Exponential Smoothing [SES.ipynb](SES.ipynb)
* Holts Winters [SW.ipynb](SW.ipynb)
* Autoregressive Integrated Moving Average [ARIMA.ipynb](ARIMA.ipynb)
* Recurrent Neural Networks [RNN.ipynb](RNN.ipynb)
* Long Short Term Memory cells [LSTM.ipynb](LSTM.ipynb)
* Gated Recurrent Unit cells [GRU.ipynb](GRU.ipynb)


Utility scripts

* `aws_arima.py` fits ARIMA model on last one month's data and forecasts load for each day
* `aws_rnn.py` fits RNN, LSTM, GRU on last 2 month's data and forecasts load for each day
* `aws_smoothing.py` fits SES, SMA, WMA on last one month's data and forecasts load for each day
* `aws.py` a scheduler to run all above three scripts everyday 00:30 IST
* `pdq_search.py` for grid search of hyperparameters of ARIMA model on last one month's data
* `load_scrap.py` to scrap load from SLDC's website
* `wheather_scrap.py` to scrap wheather data from wunderground website

