# Binance Futures API library for Python
Python library for Binance Futures and Binance Futures Testnet

That library contains just a description of code.
If you want to know what does certain function use and returns you can find more on
    https://binance-docs.github.io/apidocs/futures/en

To install Python package from github, you need to clone that repository (not installable yet).

    git clone https://github.com/morozdima/BinanceFuturesPy.git
Then just run the setup.py file from that directory,

    sudo python setup.py install

## Example
Make a new order:

```python
api_key = 'STxyXUP45HPK68ZUaZkZ6AJkMjFTVFzq'
secret_key = '398E491767030BD8A2FF6EA6D0BCB862'

client = Client(api_key=api_key, 
                sec_key=secret_key,
                symbol='BTCUSDT',
                testnet=False)

client.new_order(side='BUY',
                 quantity=0.001,
                 price=7500,
                 orderType='LIMIT',
                 timeInForce='GTC')
```

response:
```python
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
```
Close order:
```python
    client.cancel_order(173413147)
```
response:
```python
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
  ```
