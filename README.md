# Binance Futures API library for Python
Python library for Binance Futures and Binance Futures Testnet

That library contains just a description of code.
If you want to know what does certain function use and returns you can find more on
    https://binance-docs.github.io/apidocs/futures/en

To install via pip:
    pip install git+https://github.com/morozdima/BinanceFuturesPy.git

# Example
Make a new order:

    api_key = 'STxyXUP45HPK68ZUaZkZ6AJkMjFTVFzq'
    secret_key = '398E491767030BD8A2FF6EA6D0BCB862'

    client = Client(api_key=api_key, 
                    sec_key=secret_key,
                    symbol='BTCUSDT,
                    testnet=False)

    client.new_order(side='BUY',
                     quantity=0.001,
                     price=7500,
                     orderType='LIMIT',
                     timeInForce='GTC')
response:

    {'orderId': 173413147,
     'symbol': 'BTCUSDT',
     'status': 'NEW',
     'clientOrderId': 'QgJ37GrnrBibqoaGi73WFG',
     'price': '7500',
     'origQty': '0.001',
     'executedQty': '0',
     'cumQty': '0',
     'cumQuote': '0',
     'timeInForce': 'GTC',
     'type': 'LIMIT',
     'reduceOnly': False,
     'side': 'BUY',
     'stopPrice': '0',
     'workingType': 'CONTRACT_PRICE',
     'origType': 'LIMIT',
     'updateTime': 1574078626955}
     
Close order:
    
    client.cancel_order(173413147)
response:

    {'orderId': 173413147,
     'symbol': 'BTCUSDT',
     'status': 'CANCELED',
     'clientOrderId': 'DgJ15GrnrRibqoaDi86WFG',
     'price': '7500',
     'origQty': '0.001',
     'executedQty': '0',
     'cumQty': '0',
     'cumQuote': '0',
     'timeInForce': 'GTC',
     'type': 'LIMIT',
     'reduceOnly': False,
     'side': 'BUY',
     'stopPrice': '0',
     'workingType': 'CONTRACT_PRICE',
     'origType': 'LIMIT',
     'updateTime': 1574078761226}
  
  
