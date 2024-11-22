from flask import Flask, jsonify, request
import uuid
import requests

app = Flask(__name__)

stocks = {}

@app.route('/stocks', methods=['GET'])
def getStocks():
    try:
        return jsonify(list(stocks.values())), 200
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"server error": str(e)}), 500

@app.route('/stocks', methods=['POST'])
def addStock():
    try:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({"error": "Expected application/json media type"}), 415
        
        data = request.get_json()

        required_fields = ['symbol', 'purchase_price', 'shares']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Generating a unique ID for the stock
        newId = str(uuid.uuid4())

        name = data.get('name', 'NA')
        purchase_date = data.get('purchase_date', 'NA')

        if not isinstance(data['purchase_price'], (float, int)) or not isinstance(data['shares'], int):
            return jsonify({"error": "purchase_price should be a number and shares should be an integer"}), 400

        stock = {
            'id': newId,
            'name': name,
            'symbol': data['symbol'],
            'purchase_price': data['purchase_price'],
            'purchase_date': purchase_date,
            'shares': data['shares']
        }

        stocks[newId] = stock
        response_data = {"id": newId}
        return jsonify(response_data), 201
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"server error": str(e)}), 500

@app.route('/stocks/<stock_id>', methods=['GET'])
def getStock(stock_id):
    try:
        stock = stocks[stock_id]
    except KeyError:
        return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": "Internal server error"}), 500
    return jsonify(stock), 200

@app.route('/stocks/<stock_id>', methods=['DELETE'])
def delStock(stock_id):
    try:
        del stocks[stock_id]
        return '', 204
    except KeyError:
        return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": "Internal server error"}), 500

@app.route('/stocks/<stock_id>', methods=['PUT'])
def updateStock(stock_id):
    try:
        if stock_id not in stocks:
            return jsonify({"error": "Stock not found"}), 404
        
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return jsonify({"error": "Expected application/json media type"}), 415
        data = request.get_json()

        required_fields = ['symbol', 'purchase_price', 'shares']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        name = data.get('name', 'NA')
        purchase_date = data.get('purchase_date', 'NA')

        if not isinstance(data['purchase_price'], (float, int)) or not isinstance(data['shares'], int):
            return jsonify({"error": "purchase_price should be a number and shares should be an integer"}), 400

        stock = {
            'id': stock_id,
            'name': name,
            'symbol': data['symbol'],
            'purchase_price': data['purchase_price'],
            'purchase_date': purchase_date,
            'shares': data['shares']
        }

        stocks[stock_id] = stock
        response_data = {"id": stock_id}
        return jsonify(response_data), 200
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"server error": str(e)}), 500
    
@app.route('/stock-value/<stock_id>', methods=['GET'])
def getStockValue(stock_id):
    try:
        stock = stocks[stock_id]
        symbol = stock['symbol']
        shares = stock['shares']

        api_url = 'https://api.api-ninjas.com/v1/stockprice?ticker={}'.format(symbol)
        api_key = 'w1sLxL3bAN8PgoQY9wap0w==2RArL5FHfhmGgxe1'  # TODO: hide the key in env as Daniel asked

        response = requests.get(api_url, headers={'X-Api-Key': api_key})
        if response.status_code == requests.codes.ok:
            ticker = response.json()['price']
            stock_value = shares * ticker
            stock_value = {
                'symbol': symbol,
                'ticker': ticker,
                'stock_value': stock_value
            }
            return jsonify(stock_value), 200
        else:
            return jsonify({"error": "Failed to fetch stock price"}), response.status_code
    except KeyError:
        return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": "Internal server error"}), 500