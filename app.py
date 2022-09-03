
from BacktestingForecaster import BacktestingForecaster
from flask import Flask, jsonify

app = Flask(__name__)
forecaster = BacktestingForecaster()

@app.route('/btc/predict/days', methods=['GET'])
def predict():
    high_pred = forecaster.predict_btc_1d(8, True).to_frame()
    low_pred = forecaster.predict_btc_1d(8, True)
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

@app.route('/btc/train/days', methods=['POST'])
def train_btc_days():
    forecaster.train_btc_1d(True) 
    forecaster.train_btc_1d(False) 
    
    return jsonify('OK')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
