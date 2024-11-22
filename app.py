from flask import Flask, jsonify, request
import uuid

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
