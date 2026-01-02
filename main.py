from flask import Flask, request, jsonify  # 'from' ചെറിയ അക്ഷരത്തിൽ
from binance.client import Client
import json

app = Flask(__name__)

API_KEY = 'zXB5QTfURCXjnaV88to695fTqdQwBnApodwLuyl9szMISgze90cdTDFXkbYAdpsD'
API_SECRET = 'BIAuNJJN9N81GNpm5btLiRXYJghsK8CGjYNlc5W439Iou7BvcXVd8H53aamQAD20'

client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # JSON ഡാറ്റ നേരിട്ട് എടുക്കുന്നു
        data = request.get_json() 
        if not data:
            print("No JSON data received")
            return jsonify({"status": "error", "message": "Missing JSON"}), 400
            
        print(f"Received data: {data}") # ലോഗിൽ ഡാറ്റ കാണാൻ ഇത് സഹായിക്കും

        side = data.get('side').upper()
        symbol = "ETHUSDT"
        
        if side == "BUY":
            print(f"Executing BUY order for {symbol}...")
            order = client.create_order(
                symbol=symbol,
                side='BUY',
                type='MARKET',
                quoteOrderQty=10
            )
        
        elif side == "SELL":
            balance = client.get_asset_balance(asset='ETH')
            quantity_to_sell = float(balance['free'])
            
            if quantity_to_sell > 0:
                print(f"Executing SELL order for {quantity_to_sell} ETH...")
                order = client.create_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    quantity=quantity_to_sell
                )
            else:
                return jsonify({"status": "error", "message": "No ETH balance"}), 400

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
