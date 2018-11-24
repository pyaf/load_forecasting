from estimator import *

class HoltWintersEstimator(Estimator):
    """ A class that implements the Holt-Winters model for estimation. 
    Attributes:
        number_of_seasons: Number of seasons in the time series. If you have 3 years of observations, with month by month data, number_of_seasons=3.
        season_size: Indicates the number of observations in each season. For example, if you have 3 years of observation, with month by month data, season_size=12, which is the number of months in a year.
        seasonal_factor: Indicates the seasonal factor of each observation on your data set.
        average_component: Indicates the average component in the Holt-Winters model.
        tendence_component: Indicates the tendence component in the Holt-Winters model.
        seasonal_component: Indicates the seasonal component in the Holt-Winters model. It is a matrix whose first index is the seasonal index of a given time, and the second index is the season itself. 
    """

    def __init__(self, time_series, number_of_seasons, season_size):
        """ Initializes a Holt-Winters estimator. """
        super(HoltWintersEstimator, self).setTimeSeries(time_series)
        self.number_of_seasons = number_of_seasons
        self.season_size = season_size
        self.seasonal_factor = []
        self.average_component = []
        self.tendence_component = []
        self.seasonal_component = []
        self.initializeComponents()
        self.calculateComponents(0.2, 0.15, 0.05)

    def seasonOfTime(self, time):
        """ Returns the season which holds the data at a given time, from 1 to number_of_seasons """
        if (time % self.season_size) is 0:
            return int((time / self.season_size))
        return int((time / self.season_size)) + 1

    def seasonalIndexOfTime(self, time):
        """ Returns the seasonal correspondence of time, from 1 to season_size. 
        For example, if 24 month-by-month observations were made and time=13, 
        it corresponds to the first element of the season it belongs to. """
        seasonal_index = time % (self.season_size)
        if seasonal_index is 0:
            seasonal_index = self.season_size
        return seasonal_index

    def seasonMovingAverage(self, season):
        """ Returns the moving average of a season. """
        floor = (season - 1) * self.season_size
        ceil = season * self.season_size
        moving_average = 0.0

        for y in self.time_series[floor:ceil]:
            moving_average += y
        return moving_average/self.season_size
    
    def seasonalFactor(self, time):
        """ Calculates the seasonal factor for each historical data in the time series."""
        season = self.seasonOfTime(time)
        moving_average = self.seasonMovingAverage(season)
        seasonal_index = self.seasonalIndexOfTime(time)
        tendence_component = self.tendence_component[0]

        tendence = (((self.season_size + 1.0) / 2.0) - seasonal_index) * tendence_component
        seasonal_index_average = moving_average - tendence
        factor = (self.time_series[time - 1] / seasonal_index_average)

        return factor

    def insertSeasonalComponent(self, seasonal_index, season, value):
        """ Inserts a value in the seasonal component matrix.
        """
        if (len(self.seasonal_component)) < seasonal_index:
            while len(self.seasonal_component) < seasonal_index:
                self.seasonal_component.append([])
        
        if len(self.seasonal_component[seasonal_index - 1]) < (season + 1):
            while len(self.seasonal_component[seasonal_index - 1]) < (season + 1):
                self.seasonal_component[seasonal_index - 1].append(None)
        self.seasonal_component[seasonal_index - 1][season] = value

    def getSeasonalComponent(self, time):
        """ Returns a value from the seasonal component matrix.
        """
        if time <= 0:
            season = 0
            seasonal_index = self.seasonalIndexOfTime(time + self.season_size)
        else:
            seasonal_index = self.seasonalIndexOfTime(time)
            season = self.seasonOfTime(time)
        return self.seasonal_component[seasonal_index - 1][season]

    def estimate(self, time, base_time):
        """ Estimate the value of the function on time, based on the base_time observation. Often base_time is time-1. """
        estimation = (self.average_component[base_time] + self.tendence_component[base_time] * (time - base_time)) * self.getSeasonalComponent(time - self.season_size)
        return estimation

    def initializeComponents(self):
        """ Initializes the components of the Holt-Winters model. """
        first_season_average = self.seasonMovingAverage(1)
        last_season_average = self.seasonMovingAverage(self.number_of_seasons)

        #tendence component
        self.tendence_component.append((last_season_average - first_season_average) / ((self.number_of_seasons - 1) * self.season_size))
        
        #average component
        self.average_component.append( first_season_average - ((self.season_size / 2.0) * self.tendence_component[0]))
        
        #seasonal component
        for time in range(1, len(self.time_series) + 1):
            self.seasonal_factor.append(self.seasonalFactor(time))

        
        seasonal_index_average = []
        for seasonal_index in range(1, self.season_size + 1):
            seasonal_index_sum = 0.0
            for m in range(self.number_of_seasons):
                index = seasonal_index + (m * self.season_size)
                factor = self.seasonal_factor[index - 1]
                seasonal_index_sum += factor
            seasonal_index_average.append(seasonal_index_sum *  (1.0 / self.number_of_seasons))

        snt_average_sum = 0.0
        for snt_average in seasonal_index_average:
            snt_average_sum += snt_average
        adjustment_level = self.season_size / snt_average_sum

        for seasonal_index in range(1, self.season_size + 1):
            value = seasonal_index_average[seasonal_index - 1] * adjustment_level
            self.insertSeasonalComponent(seasonal_index, 0, value)

    def calculateComponents(self, alpha, beta, gamma):
        for time in range(1, len(self.time_series) + 1):
            average_component = (alpha * (self.time_series[time - 1] / self.getSeasonalComponent(time - self.season_size))) + ((1 - alpha) * (self.average_component[time - 1] + self.tendence_component[time - 1]))
            self.average_component.append(average_component)

            tendence_component = (beta * (self.average_component[time] - self.average_component[time - 1])) + ((1 - beta) * self.tendence_component[time - 1])
            self.tendence_component.append(tendence_component)

            seasonal_component = gamma * self.time_series[time - 1] / self.average_component[time] + (1 - gamma) * self.getSeasonalComponent(time - self.season_size)
            index = self.seasonalIndexOfTime(time)
            season = self.seasonOfTime(time)
            self.insertSeasonalComponent(index, season, seasonal_component)

time_series_soda = [189, 229, 249, 289, 260, 431, 660, 777, 915, 613, 485, 277, 244, 296, 319, 370, 313, 556, 831, 960, 1152, 759, 607, 371, 298, 378, 373, 443, 374, 660, 1004, 1153, 1388, 904, 715, 441]
hwe = HoltWintersEstimator(time_series_soda, 3, 12)
