

from forecasters.BacktestingForecaster import BacktestingForecaster
from forecasters.BacktestingForecaster import BacktestingForecaster

class BTCBacktestingForecaster:    
    LAG = 1000
    
    HIGH_FILENAME = 'btc_high.sav'
    LOW_FILENAME = 'btc_low.sav'
    
    def predict(self, steps, high_values):
        forecaster = BacktestingForecaster.load_model(self.HIGH_FILENAME if high_values else self.LOW_FILENAME)
        return forecaster.predict(steps=steps)
    
    def train(self, high_values):
        url = 'https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=1410825600&period2=' + BacktestingForecaster.get_yesterday_epoch() + '&interval=1d&events=history&includeAdjustedClose=true'
        column_to_use = ('High' if high_values else 'Low')
        forecaster = BacktestingForecaster.train(url, column_to_use, 1, self.LAG)
        filename = (self.HIGH_FILENAME if high_values else self.LOW_FILENAME)
        BacktestingForecaster.save_model(forecaster, filename)