@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # force=True നൽകുന്നത് തെറ്റായ ഫോർമാറ്റുകളെപ്പോലും വായിക്കാൻ സഹായിക്കും
        data = request.get_json(force=True)
        
        if not data:
            print("Received empty or invalid data")
            return "Invalid Data", 400

        print(f"Data received successfully: {data}")
        # ... ബാക്കി കോഡ് ...
