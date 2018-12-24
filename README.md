# Electric Load Forecasting

Under graduate project on short term electric load forecasting. Data was taken from [State Load Despatch Center, Delhi](www.delhisldc.org/) website and multiple time series algorithms were implemented during the course of the project.

### Models implemented:

`models` folder contains all the algorithms/models implemented during the course of the project:

* Feed forward Neural Network [FFNN.ipynb](FFNN.ipynb)
* Simple Moving Average [SMA.ipynb](SMA.ipynb)
* Weighted Moving Average [WMA.ipynb](WMA.ipynb)
* Simple Exponential Smoothing [SES.ipynb](SES.ipynb)
* Holts Winters [HW.ipynb](HW.ipynb)
* Autoregressive Integrated Moving Average [ARIMA.ipynb](ARIMA.ipynb)
* Recurrent Neural Networks [RNN.ipynb](RNN.ipynb)
* Long Short Term Memory cells [LSTM.ipynb](LSTM.ipynb)
* Gated Recurrent Unit cells [GRU.ipynb](GRU.ipynb)

scripts:

* `aws_arima.py` fits ARIMA model on last one month's data and forecasts load for each day.
* `aws_rnn.py` fits RNN, LSTM, GRU on last 2 month's data and forecasts load for each day.
* `aws_smoothing.py` fits SES, SMA, WMA on last one month's data and forecasts load for each day.
* `aws.py` a scheduler to run all above three scripts everyday 00:30 IST.
* `pdq_search.py` for grid search of hyperparameters of ARIMA model on last one month's data.
* `load_scrap.py` scraps day wise load data of Delhi from [SLDC](https://www.delhisldc.org/Loaddata.aspx?mode=17/01/2018) site and stores it in csv format.
* `wheather_scrap.py` scraps day wise whether data of Delhi from [wunderground](https://www.wunderground.com/history/airport/VIDP/2017/8/1/DailyHistory.html) site and stores it in csv format.

`server` folder contains django webserver code, developed to show the implemented algorithms and compare their performance. All the implemented algorithms are being used to forecast today's Delhi electricity load [here](http://forecast.energyandsystems.com). Project report can be found in [Report](Report) folder. 

![A screenshot of the website](screenshots/website.png "A screenshot of the website")


### Team Members:

* Ayush Kumar Goyal
* Boragapu Sunil Kumar
* Srimukha Paturi
* Rishabh Agrahari
