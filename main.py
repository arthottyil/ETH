from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# നിങ്ങളുടെ ബൈനൻസ് കീകൾ ഇവിടെ നൽകുക
API_KEY = 'zXB5QTfURCXjnaV88to695fTqdQwBnApodwLuyl9szMISgze90cdTDFXkbYAdpsD'
API_SECRET = 'BIAuNJJN9N81GNpm5btLiRXYJghsK8CGjYNlc5W439Iou7BvcXVd8H53aamQAD20'

client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # ഡാറ്റ JSON ആയിട്ടല്ലെങ്കിൽ വെറും ടെക്സ്റ്റ് ആയി എടുക്കുന്നു
        raw_data = request.get_data(as_text=True).lower()
        print(f"Raw data received: {raw_data}")

        symbol = "ETHUSDT"
        
        # ഡാറ്റയിൽ 'buy' എന്ന വാക്കുണ്ടോ എന്ന് നോക്കുന്നു
        if 'buy' in raw_data:
            print("Executing BUY order...")
            order = client.create_order(symbol=symbol, side='BUY', type='MARKET', quoteOrderQty=10)
            return jsonify({"status": "success", "action": "buy"}), 200
            
        # ഡാറ്റയിൽ 'sell' എന്ന വാക്കുണ്ടോ എന്ന് നോക്കുന്നു
        elif 'sell' in raw_data:
            balance = client.get_asset_balance(asset='ETH')
            qty = float(balance['free'])
            if qty > 0:
                print(f"Executing SELL order for {qty} ETH...")
                order = client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=qty)
                return jsonify({"status": "success", "action": "sell"}), 200
            else:
                return jsonify({"status": "error", "message": "No balance"}), 200
        
        else:
            print("No valid command found in data")
            return jsonify({"status": "ignored"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
