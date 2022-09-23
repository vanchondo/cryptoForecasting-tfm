import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from forecasters.ADABacktestingForecaster import ADABacktestingForecaster
from forecasters.BTCBacktestingForecaster import BTCBacktestingForecaster
from forecasters.ETHBacktestingForecaster import ETHBacktestingForecaster
from forecasters.SOLBacktestingForecaster import SOLBacktestingForecaster
from forecasters.XRPBacktestingForecaster import XRPBacktestingForecaster
from flask import Flask, jsonify, g

app = Flask(__name__)
btcForecaster = BTCBacktestingForecaster()
ethForecaster = ETHBacktestingForecaster()
adaForecaster = ADABacktestingForecaster()
xrpForecaster = XRPBacktestingForecaster()
solForecaster = SOLBacktestingForecaster()

days_ahead = 8

@app.route('/predict/btc', methods=['GET'])
def predictBTC():
    high_pred = btcForecaster.predict(days_ahead, True).to_frame()
    low_pred = btcForecaster.predict(days_ahead, False)
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

@app.route('/predict/eth', methods=['GET'])
def predictETH():
    high_pred = ethForecaster.predict(days_ahead, True).to_frame()
    low_pred = ethForecaster.predict(days_ahead, False)
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

@app.route('/predict/ada', methods=['GET'])
def predictADA():
    high_pred = adaForecaster.predict(days_ahead, True).to_frame()
    low_pred = adaForecaster.predict(days_ahead, False)
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

@app.route('/predict/xrp', methods=['GET'])
def predictXRP():
    high_pred = xrpForecaster.predict(days_ahead, True).to_frame()
    low_pred = xrpForecaster.predict(days_ahead, False)
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

@app.route('/predict/sol', methods=['GET'])
def predictSOL():
    high_pred = solForecaster.predict(days_ahead, True).to_frame()
    low_pred = solForecaster.predict(days_ahead, False)
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
    btcForecaster.train(True) 
    btcForecaster.train(False)
    ethForecaster.train(True)
    ethForecaster.train(False)
    adaForecaster.train(True)
    adaForecaster.train(False)
    xrpForecaster.train(True)
    xrpForecaster.train(False)
    solForecaster.train(True)
    solForecaster.train(False)

trainAll()
scheduler = BackgroundScheduler()
scheduler.add_job(func=trainAll, trigger="interval", hours=4)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
