
# from pyramid.arima import auto_arima
import pandas as pd
import logging
import itertools
import numpy as np
import statsmodels.api as sm
import warnings

warnings.filterwarnings("ignore") # specify to ignore warning messages

# to store the log in a file called 'arima_log.txt'
logging.basicConfig(
    filename='pdq_log.txt',
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)
logger = logging.getLogger()
console = logging.StreamHandler()
logger.addHandler(console)

data = pd.read_csv('monthdata.csv', header=None, index_col=['datetime'], names=['datetime', 'load'], parse_dates=['datetime'], infer_datetime_format=True)
data = data.asfreq(freq='H', method='bfill')  # sample the data in hourly manner


# Define the p, d and q parameters to take any value between 0 and 3
p = d = q = range(0, 3)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 24) for x in list(itertools.product(p, d, q))]

logger.info('pdq:')
logger.info(pdq)
logger.info('seasonal_pdq')
logger.info(seasonal_pdq)

bestAIC = np.inf
bestParam = None
bestSParam = None

logger.info('Running GridSearch')

#use gridsearch to look for optimial arima parameters
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(data,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()
            logger.info('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))

            #if current run of AIC is better than the best one so far, overwrite it
            if results.aic < bestAIC:
                bestAIC = results.aic
                bestParam = param
                bestSParam = param_seasonal

        except Exception as e:
        	print(e)

            
logger.info('the best bestAIC, bestParam, bestSParam:')
logger.info(bestAIC)
logger.info(bestParam)
logger.info(bestSParam)
