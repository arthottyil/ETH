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
    # ഡാറ്റ എന്ത് വന്നാലും എറർ അടിക്കാതെ സ്വീകരിക്കുന്നു
    raw_data = request.get_data(as_text=True).lower()
    print(f"Signal Received: {raw_data}")

    symbol = "ETHUSDT"
    
    try:
        if 'buy' in raw_data:
            print("Processing BUY...")
            client.create_order(symbol=symbol, side='BUY', type='MARKET', quoteOrderQty=10)
            return "Success Buy", 200
        elif 'sell' in raw_data:
            print("Processing SELL...")
            balance = client.get_asset_balance(asset='ETH')
            qty = float(balance['free'])
            if qty > 0:
                client.create_order(symbol=symbol, side='SELL', type='MARKET', quantity=qty)
                return "Success Sell", 200
            return "No Balance", 200
    except Exception as e:
        print(f"Binance Error: {str(e)}")
        return str(e), 200 # എറർ വന്നാലും 200 നൽകുന്നു (400 ഒഴിവാക്കാൻ)

    return "Ignored", 200

if __name__ == '__main__':
    # Render-ൽ 10000 ആണ് സാധാരണ പോർട്ട്
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
