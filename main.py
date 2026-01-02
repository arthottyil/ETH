from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# Binance Keys
API_KEY = 'zXB5QTfURCXjnaV88to695fTqdQwBnApodwLuyl9szMISgze90cdTDFXkbYAdpsD'
API_SECRET = 'BIAuNJJN9N81GNpm5btLiRXYJghsK8CGjYNlc5W439Iou7BvcXVd8H53aamQAD20'

client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # force=True നൽകുന്നത് തെറ്റായ ഫോർമാറ്റുകളെപ്പോലും വായിക്കാൻ സഹായിക്കും
        data = request.get_json(force=True)
        
        if not data:
            print("Received empty or invalid data")
            return "Invalid Data", 400

        print(f"Data received successfully: {data}") # ഇത് ലോഗിൽ കാണാൻ സാധിക്കും

        side = data.get('side').upper()
        symbol = "ETHUSDT"
        
        if side == "BUY":
            print("Processing BUY Order...")
            order = client.create_order(
                symbol=symbol,
                side='BUY',
                type='MARKET',
                quoteOrderQty=10 # 10 USDT-ക്ക് വാങ്ങുന്നു
            )
            print("BUY Order Successful")
            
        elif side == "SELL":
            print("Processing SELL Order...")
            balance = client.get_asset_balance(asset='ETH')
            qty = float(balance['free'])
            
            # ബൈനൻസിലെ ലോട്ടറി സൈസ് അനുസരിച്ച് അളവ് ക്രമീകരിക്കുന്നു (ഉദാ: 4 ഡെസിമൽ)
            qty = floor(qty * 10000) / 10000 
            
            if qty > 0.0001: # വിൽക്കാൻ മിനിമം ബാലൻസ് ഉണ്ടോ എന്ന് നോക്കുന്നു
                order = client.create_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    quantity=qty
                )
                print("SELL Order Successful")
            else:
                print("Error: Insufficient ETH Balance to Sell")

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"Final Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
