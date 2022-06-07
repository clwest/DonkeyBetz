import ccxt  

ftx = ccxt.ftx()

def get_quote(request):
    symbol = request.args.get('symbol')

    try:
        quote = ftx.fetch_ticker(symbol)
    except Exception as e:
        return {
            "code": "error",
            "message": str(e)
        }
    
    return quote