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
        # ഡാറ്റ കിട്ടുന്നുണ്ടോ എന്ന് പരിശോധിക്കുന്നു
        raw_data = request.data.decode('utf-8').strip()
        print(f"Raw data received: {raw_data}")

        # JSON ആയി വായിക്കാൻ ശ്രമിക്കുന്നു, പരാജയപ്പെട്ടാൽ സാധാരണ ടെക്സ്റ്റ് ആയി എടുക്കുന്നു
        try:
            data = json.loads(raw_data)
        except:
            data = {"side": raw_data.lower()}

        print(f"Processed Data: {data}")
        side = data.get('side', '').upper()
        symbol = "ETHUSDT"
        
        if side == "BUY":
            print(f"Executing BUY order for {symbol}...")
            order = client.create_order(
                symbol=symbol,
                side='BUY',
                type='MARKET',
                quoteOrderQty=10
            )
            print("Order Success!")
        
        elif side == "SELL":
            balance = client.get_asset_balance(asset='ETH')
            qty = float(balance['free'])
            if qty > 0:
                print(f"Executing SELL order for {qty} ETH...")
                order = client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=qty)
                print("Order Success!")
            else:
                return jsonify({"status": "error", "message": "No balance"}), 400

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Render നൽകുന്ന പോർട്ട് ഉപയോഗിക്കുന്നു
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
