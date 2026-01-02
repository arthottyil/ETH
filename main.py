from flask import Flask, request, jsonify
from binance.client import Client
import json
import os

app = Flask(__name__)

# നിങ്ങളുടെ ബൈനൻസ് കീകൾ ഇവിടെ കൃത്യമായി നൽകുക
# ശ്രദ്ധിക്കുക: ഇതിൽ അനാവശ്യ സ്പേസുകളോ ചിഹ്നങ്ങളോ ഇല്ലെന്ന് ഉറപ്പാക്കുക
API_KEY = 'zXB5QTfURCXjnaV88to695fTqdQwBnApodwLuyl9szMISgze90cdTDFXkbYAdpsD'
API_SECRET = 'BIAuNJJN9N81GNpm5btLiRXYJghsK8CGjYNlc5W439Iou7BvcXVd8H53aamQAD20'

client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # JSON ഡാറ്റ ഏത് ഫോർമാറ്റിൽ വന്നാലും സ്വീകരിക്കാൻ 'force=True' സഹായിക്കും
        data = request.get_json(silent=True, force=True)
        
        # ഡാറ്റ കിട്ടിയില്ലെങ്കിൽ റോ (Raw) ഡാറ്റയിൽ നിന്ന് എടുക്കാൻ ശ്രമിക്കുന്നു
        if data is None:
            raw_data = request.data.decode('utf-8')
            print(f"Raw data received: {raw_data}")
            data = json.loads(raw_data)

        print(f"Final Data to process: {data}")
        
        side = data.get('side', '').upper()
        symbol = "ETHUSDT"
        
        if side == "BUY":
            print(f"Executing BUY order for {symbol} using 10 USDT...")
            order = client.create_order(
                symbol=symbol,
                side='BUY',
                type='MARKET',
                quoteOrderQty=10
            )
            print("BUY Order Success!")
        
        elif side == "SELL":
            balance = client.get_asset_balance(asset='ETH')
            qty = float(balance['free'])
            
            if qty > 0:
                print(f"Executing SELL order for {qty} ETH...")
                order = client.create_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    quantity=qty
                )
                print("SELL Order Success!")
            else:
                return jsonify({"status": "error", "message": "No ETH balance to sell"}), 400

        return jsonify({"status": "success", "message": "Order Executed"}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        # എറർ വരുമ്പോൾ ലോഗിൽ വ്യക്തമായി കാണാൻ ഇത് സഹായിക്കും
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Render നൽകുന്ന പോർട്ട് ഉപയോഗിക്കുന്നു, അല്ലെങ്കിൽ 8080 എടുക്കുന്നു
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
