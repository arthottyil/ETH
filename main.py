from flask import Flask, request, jsonify
from binance.client import Client
import json
import os

app = Flask(__name__)

# നിങ്ങളുടെ ബൈനൻസ് കീകൾ ഇവിടെ നൽകുക
API_KEY = 'zXB5QTfURCXjnaV88to695fTqdQwBnApodwLuyl9szMISgze90cdTDFXkbYAdpsD'
API_SECRET = 'BIAuNJJN9N81GNpm5btLiRXYJghsK8CGjYNlc5W439Iou7BvcXVd8H53aamQAD20'

client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # ഡാറ്റ എങ്ങനെ വന്നാലും അത് വായിക്കുന്നു
        raw_data = request.get_data(as_text=True).strip()
        print(f"Raw data received: {raw_data}")

        # 'buy' അല്ലെങ്കിൽ 'sell' എന്ന് മാത്രമാണോ വന്നതെന്ന് നോക്കുന്നു
        if 'buy' in raw_data.lower():
            side = 'BUY'
        elif 'sell' in raw_data.lower():
            side = 'SELL'
        else:
            # JSON ആയി വന്നാൽ അത് വായിക്കുന്നു
            try:
                data = json.loads(raw_data)
                side = data.get('side', '').upper()
            except:
                return jsonify({"status": "error", "message": "Invalid format"}), 400

        symbol = "ETHUSDT"
        if side == "BUY":
            print(f"Executing BUY order...")
            order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quoteOrderQty=10)
            print("Order Success!")
        elif side == "SELL":
            balance = client.get_asset_balance(asset='ETH')
            qty = float(balance['free'])
            if qty > 0:
                order = client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=qty)
                print("Order Success!")
            else:
                return jsonify({"status": "error", "message": "No ETH balance"}), 400

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
