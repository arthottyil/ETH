from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# നിങ്ങളുടെ API Keys (സ്പേസ് ഇല്ലെന്ന് ഉറപ്പാക്കുക)
API_KEY = 'zXB5QTfURCXjnaV88to695fTqdQwBnApodwLuyl9szMISgze90cdTDFXkbYAdpsD'.strip()
API_SECRET = 'BIAuNJJN9N81GNpm5btLiRXYJghsK8CGjYNlc5W439Iou7BvcXVd8H53aamQAD20'.strip()

# ലൊക്കേഷൻ എറർ ഒഴിവാക്കാൻ സർവർ സമയം സിങ്ക് ചെയ്യുന്നു
client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # സിഗ്നൽ സ്വീകരിക്കുന്നു
        raw_data = request.get_data(as_text=True).lower()
        print(f"Signal: {raw_data}")

        symbol = "ETHUSDT"
        
        if 'buy' in raw_data:
            print("Buying ETH...")
            # പത്തൊൻപത് USDT ഓർഡർ ചെയ്യുന്നു
            order = client.create_order(
                symbol=symbol,
                side='BUY',
                type='MARKET',
                quoteOrderQty=10
            )
            print("Buy Success!")
            return jsonify({"status": "success"}), 200

        elif 'sell' in raw_data:
            print("Selling ETH...")
            balance = client.get_asset_balance(asset='ETH')
            qty = float(balance['free'])
            if qty > 0:
                order = client.create_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    quantity=qty
                )
                print("Sell Success!")
                return jsonify({"status": "success"}), 200
            return "No Balance", 200

        return "No action", 200

    except Exception as e:
        # എറർ എന്താണെന്ന് ലോഗിൽ കൃത്യമായി കാണിക്കും
        print(f"Detailed Error: {str(e)}")
        return str(e), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
