import pandas as pd
import matplotlib.pyplot as plt

def extract_dt(data):
    data['time'] += ':00'
    data['datetime'] = pd.to_timedelta(data['time'])
    data['hour'] = data['datetime'].dt.seconds // 3600 
    return data

def plot_curves(day_range, month, year):
    data = {}
    for day in day_range:
        date = '%02d-%02d-%d' % (day, month, year)
        data['df%02d' % day] = extract_dt(pd.read_csv('SLDC_Data/%d/%02d/%s.csv' % (year, month, date)))
        data['df%02d' % day]['date'] = date

    fig = plt.figure(figsize=(20, 10))
    date = []
    for i in sorted(data):
        frame = data[i]
        plt.plot(frame['time'], frame['value']);
        date.append(frame['date'][0])
    plt.legend(date, loc='best');
    plt.show()
    

if __name__=='main':
    pass