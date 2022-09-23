import io
import urllib.request
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import pickle
import pandas as pd
from lightgbm import LGBMRegressor
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.model_selection import backtesting_forecaster

class BacktestingForecaster:
    def train(url, column_to_use, steps, lag):
        data = BacktestingForecaster.download_file(url)
        data = BacktestingForecaster.clean_data(data, column_to_use)
        start_train, end_train = BacktestingForecaster.getLimitDates(data)
        predictions, metric, forecaster = BacktestingForecaster.train_backtesting_forecaster(lag, steps, data, column_to_use, start_train, end_train)

        return forecaster    
    
    def train_backtesting_forecaster(lag, steps, data, column, start_train, end_train):        
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

    def clean_data(data, column):
        data['Date'] = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
        data = data.loc[:, ['Date', column]]
        data = data.set_index('Date')
        data = data.asfreq('D')
        data = data.sort_index()
        
        return data

    def get_yesterday_epoch():
        d = date.today() - timedelta(days=1)
        return str(datetime(d.year, d.month, d.day).timestamp()).replace('.0', '')

    def getLimitDates(datos):           
        trainStartDate = datos.index.min()
        trainEndDate =  (datetime.now() - relativedelta(days = 2)).strftime('%Y-%m-%d')

        return (
            trainStartDate,
            trainEndDate
        )

    def download_file(url):
        with urllib.request.urlopen(url) as f:
            response = f.read().decode('utf-8')
        data = pd.read_csv(io.StringIO(response))
        data = data.set_index("Date")
        return data
    
    def save_model(model, filename):
        pickle.dump(model, open(filename, 'wb'))
        
    def load_model(filename):
        return pickle.load(open(filename, 'rb'))