import io
import urllib.request
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import pickle
import pandas as pd
from lightgbm import LGBMRegressor
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.model_selection import backtesting_forecaster
from sklearn.metrics import mean_absolute_error

class BacktestingForecaster:
    
    LAG = 920
    BTC_1_DAY_HIGH_FILENAME = 'btc_1d_high.sav'
    BTC_1_DAY_LOW_FILENAME = 'btc_1d_low.sav'
    
    def predict_btc_1d(self, steps, high_values):
        forecaster = self.load_model(self.BTC_1_DAY_HIGH_FILENAME if high_values else self.BTC_1_DAY_LOW_FILENAME)
        return forecaster.predict(steps=steps)
    
    def train_btc_1d(self, high_values):
        forecaster = self.train_btc(1, high_values)
        filename = (self.BTC_1_DAY_HIGH_FILENAME if high_values else self.BTC_1_DAY_LOW_FILENAME)
        self.save_model(forecaster, filename)
    
    def train_btc(self, steps, high_values):
        column_to_use = ('High' if high_values else 'Low')
        btc_url = 'https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=1410825600&period2=' + self.get_yesterday_epoch() + '&interval=1d&events=history&includeAdjustedClose=true'
        data = self.download_file(btc_url)
        data = self.clean_data(data, column_to_use)
        start_train, end_train = self.getLimitDates(data)
        predictions, metric, forecaster = self.train_backtesting_forecaster(self.LAG, steps, data, column_to_use, start_train, end_train)

        return forecaster

    def train_backtesting_forecaster(self, lag, steps, data, column, start_train, end_train):        
        # Create forecaster
        forecaster = ForecasterAutoreg(
                        regressor = LGBMRegressor(random_state=123),
                        lags      = lag
                        )
        
        # Backtest test data, 1 step
        metric, predictions = backtesting_forecaster(
                                    forecaster = forecaster,
                                    y          = data.loc[start_train:, column],
                                    initial_train_size = len(data.loc[start_train:end_train, column]),
                                    fixed_train_size   = True,
                                    steps      = steps,
                                    refit      = True,
                                    metric     = 'mean_absolute_error',
                                    verbose    = False
                                    )
        
        forecaster.fit(y = data.loc[start_train:end_train, column])
        return (predictions, metric, forecaster)

    def clean_data(self, data, column):
        data['Date'] = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
        data = data.loc[:, ['Date', column]]
        data = data.set_index('Date')
        data = data.asfreq('D')
        data = data.sort_index()
        
        return data

    def get_yesterday_epoch(self):
        d = date.today() - timedelta(days=1)
        return str(datetime(d.year, d.month, d.day).timestamp()).replace('.0', '')

    def getLimitDates(self, datos):           
        trainStartDate = datos.index.min()
        trainEndDate =  (datetime.now() - relativedelta(days = 2)).strftime('%Y-%m-%d')

        return (
            trainStartDate,
            trainEndDate
        )

    def download_file(self, url):
        with urllib.request.urlopen(url) as f:
            response = f.read().decode('utf-8')
        data = pd.read_csv(io.StringIO(response))
        data = data.set_index("Date")
        return data
    
    def save_model(self, model, filename):
        pickle.dump(model, open(filename, 'wb'))
        
    def load_model(self, filename):
        return pickle.load(open(filename, 'rb'))