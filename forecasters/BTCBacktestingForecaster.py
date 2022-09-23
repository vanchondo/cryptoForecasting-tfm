

from forecasters.BacktestingForecaster import BacktestingForecaster
from forecasters.BacktestingForecaster import BacktestingForecaster

class BTCBacktestingForecaster:    
    LAG = 920
    
    BTC_HIGH_FILENAME = 'btc_high.sav'
    BTC_LOW_FILENAME = 'btc_low.sav'
    
    def predict(self, steps, high_values):
        forecaster = BacktestingForecaster.load_model(self.BTC_HIGH_FILENAME if high_values else self.BTC_LOW_FILENAME)
        return forecaster.predict(steps=steps)
    
    
    def train(self, high_values):
        btc_url = 'https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=1410825600&period2=' + BacktestingForecaster.get_yesterday_epoch() + '&interval=1d&events=history&includeAdjustedClose=true'        
        column_to_use = ('High' if high_values else 'Low')
        forecaster = BacktestingForecaster.train(btc_url, column_to_use, 1, self.LAG)
        filename = (self.BTC_HIGH_FILENAME if high_values else self.BTC_LOW_FILENAME)
        BacktestingForecaster.save_model(forecaster, filename)
