# futurespy
python library for Binance Futures and Binance Futures Testnet

That library contains just a description of code.
If you want to know what does certain function use and returns you can find more on
    https://binance-docs.github.io/apidocs/futures/en

# Example

    if __name__ == __main__:
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
