# Load and Price Forcasting

Btech Project on Load and Price forcasting.

### Code

Inside `data` folder:

* [load_scrap.py](load_scrap.py) scraps day wise load data of Delhi from [SLDC](https://www.delhisldc.org/Loaddata.aspx?mode=17/01/2018) site and stores it in csv format. 
* [whether_scrap.py](whether_scrap.py) scraps day wise whether data of Delhi from [wunderground](https://www.wunderground.com/history/airport/VIDP/2017/8/1/DailyHistory.html) site and stores it in csv format.
* [get_real_time_img.py](get_real_time_img.py) downloads real time load curve from [SLDC](https://www.delhisldc.org/Loadcurve.aspx) site.

Inside `server` folder:

Django website code.
