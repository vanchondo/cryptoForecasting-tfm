
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from BacktestingForecaster import BacktestingForecaster
from flask import Flask, jsonify, g

app = Flask(__name__)
forecaster = BacktestingForecaster()

@app.route('/btc/predict/days', methods=['GET'])
def predict():
    high_pred = forecaster.predict_btc_1d(8, True).to_frame()
    low_pred = forecaster.predict_btc_1d(8, False)
    high_pred['low'] = low_pred
    response = []
    for row in high_pred.iterrows():
        date = row[0].strftime('%Y-%m-%d')
        high = row[1][0]
        low = row[1][1]
        response.append({
            'Date' : date,
            'High' : high,
            'Low' : low
        })
        
    response.pop(0)
        
    return jsonify(response)


def trainAll():
    forecaster.train_btc_1d(True) 
    forecaster.train_btc_1d(False) 

trainAll()
scheduler = BackgroundScheduler()
scheduler.add_job(func=trainAll, trigger="cron", hour=23)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
