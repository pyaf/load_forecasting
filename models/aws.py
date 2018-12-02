import os
import schedule
import time


def job():
    os.system("./aws_arima.py 1")
    print('Done with ARIMA, running smoothing models')
    os.system("./aws_smoothing.py 1")
    print('Done with smoothing models, running RNN models')
    os.system("./aws_rnn.py 1")
    print('Done')
    return None


schedule.every().day.at("00:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute
