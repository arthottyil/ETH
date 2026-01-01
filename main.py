from flask import Flask, request, jsonify
from binance.client import Client
import json

app = Flask(__name__)

# നിങ്ങളുടെ Binance API Keys ഇവിടെ നൽകുക
API_KEY = 'zXB5QTfURCXjnaV88to695fTqdQwBnApodwLuyl9szMISgze90cdTDFXkbYAdpsD'
API_SECRET = 'BIAuNJJN9N81GNpm5btLiRXYJghsK8CGjYNlc5W439Iou7BvcXVd8H53aamQAD20'

client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = json.loads(request.data)
        side = data.get('side').upper() # BUY അല്ലെങ്കിൽ SELL
        symbol = "ETHUSDT"
        
        if side == "BUY":
            # 10 USDT മുഴുവനായി ഉപയോഗിച്ച് ETH വാങ്ങുന്നു
            print(f"Executing BUY order for {symbol} using 10 USDT...")
            order = client.create_order(
                symbol=symbol,
                side='BUY',
                type='MARKET',
                quoteOrderQty=10  # തുക USDT-യിൽ നിശ്ചയിക്കുന്നു
            )
        
        elif side == "SELL":
            # വാലറ്റിലുള്ള മുഴുവൻ ETH ബാലൻസും ചെക്ക് ചെയ്യുന്നു
            balance = client.get_asset_balance(asset='ETH')
            quantity_to_sell = float(balance['free'])
            
            # വിൽക്കാൻ മിനിമം ബാലൻസ് ഉണ്ടോ എന്ന് പരിശോധിക്കുന്നു
            if quantity_to_sell > 0:
                print(f"Executing SELL order for {quantity_to_sell} ETH...")
                order = client.create_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    quantity=quantity_to_sell
                )
            else:
                return jsonify({"status": "error", "message": "No ETH balance to sell"}), 400

        return jsonify({"status": "success", "order": "Executed"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Bot-hosting.net സാധാരണയായി 80-ാം പോർട്ടിലോ അല്ലെങ്കിൽ എൻവയറോൺമെന്റ് നൽകുന്ന പോർട്ടിലോ ആണ് പ്രവർത്തിക്കുക
    app.run(host='0.0.0.0', port=8080)
