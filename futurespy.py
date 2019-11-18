from sys import stdout
import time

import pandas as pd

import websocket
import requests
import urllib
import json


import hmac
import hashlib

'''
    That library have got just a part of Documentation
    If you want to know what does certain function use can find more on
    
    ! ! !
    https://binance-docs.github.io/apidocs/futures/en
    ! ! !
'''
class MarketData:
    
    def __init__(self, 
                 testnet: bool = False,
                 symbol: str = 'btcusdt',
                 interval: str = '1m'):
        
        '''
        
        To use TESTNET Binance Futures API  -> testnet = True
        
        To change currency pair             -> symbol = 'ethusdt'
        
        To change interval                  -> interval = '5m'
        (m -> minutes
         h -> hours
         d -> days
         w -> weeks
         M -> months;
        
        Valid values: [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M])
        
        '''


        if testnet == True:
            self.http_way = 'http://testnet.binancefuture.com/fapi/v1/'
        else:
            self.http_way = 'http://fapi.binance.com/fapi/v1/'
        
        self.wss_way = 'wss://fstream.binance.com/ws/'
        self.interval = interval
        self.symbol = symbol.lower()



    def ping(self):
        return requests.get(f'{self.http_way}ping').json()



    def server_time(self):
        return requests.get(f'{self.http_way}time').json()



    def exchange_info(self):
        return requests.get(f'{self.http_way}exchangeInfo').json()



    def order_book(self, limit: int = 100):
        '''
        To change limit -> limit = 1000
        (Valid limits:[5, 10, 20, 50, 100, 500, 1000])
        '''
        return requests.get(f'{self.http_way}depth?limit={limit}').json()
    
    
    
    def recent_trades(self, limit: int = 500):
        '''
        To change limit -> limit = 1000
        (max 1000)
        '''
        return requests.get(f'{self.http_way}trades?symbol={self.symbol}&limit={limit}').json()


    def historical_trades(self, limit: int = 500):
        '''
        To change limit -> limit = 1000
        (max 1000)
        '''
        return requests.get(f'{self.http_way}historicalTrades?symbol={self.symbol}&limit={limit}').json()



    def aggregate_trades(self, 
                         fromId: int = None,
                         startTime: int = None,
                         endTime: int = None,
                         limit: int = 500):
        '''
        To change limit                     ->  limit = 1000
        (max 1000)
        
        To use fromId                       ->  fromId = 1231
        To use start time and end time      ->  startTime = 1573661424937
                                            ->  endTime = 1573661428706
        '''
        return requests.get(f'{self.http_way}aggTrades?symbol={self.symbol}&fromId={fromId}&startTime={startTime}&endTime={endTime}&limit={limit}').json()



    def candles_data(self, 
                     interval: str = '1m',
                     startTime: int = None,
                     endTime: int = None,
                     limit: int = 500):
        '''
        To change interval                  ->  interval = '5m'
        (Valid values: [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M])
        
        To use limit                        ->  limit = 1231
        (Default 500; max 1500)
        
        To use start time and end time      ->  startTime = 1573661424937
                                            ->  endTime = 1573661428706
        '''
        return requests.get(f'{self.http_way}klines?symbol={self.symbol}&interval={interval}&startTime={startTime}&endTime={endTime}&limit={limit}').json()



    def mark_price(self):
        return requests.get(f'{self.http_way}premiumIndex?symbol={self.symbol}').json()
    
    
    
    def funding_rate(self,
                     startTime: int = None,
                     endTime: int = None,
                     limit: int = 100):
        '''
        To change limit                     ->  limit = 1000
        (max 1096)
        
        To use start time and end time      ->  startTime = 1573661424937
                                            ->  endTime = 1573661428706
        '''
        return requests.get(f'{self.http_way}klines?symbol={self.symbol}&startTime={startTime}&endTime={endTime}&limit={limit}').json()
    
    
    
    def ticker_price_24h(self, 
                         symbol: bool = False):
        if symbol is True:
            return requests.get(f'{self.http_way}ticker/24hr?symbol={self.symbol}').json()
        else:
            return requests.get(f'{self.http_way}ticker/24hr').json()
    
    
    
    def ticker_price_symbol(self, 
                            symbol: bool = False):
        if symbol is True:
            return requests.get(f'{self.http_way}ticker/price?symbol={self.symbol}').json()
        else:
            return requests.get(f'{self.http_way}ticker/price').json()
    
    
    def ticker_orderbook_symbol(self, 
                                symbol: bool = False):
        if symbol is True:
            return requests.get(f'{self.http_way}ticker/bookTicker?symbol={self.symbol}').json()
        else:
            return requests.get(f'{self.http_way}ticker/bookTicker').json()



#%%



class WebsocketMarket:
    
    def __init__(self,
                 on_message = lambda ws, message: (stdout.write(f'\r{json.loads(message)}'), stdout.flush()),
                 on_error = lambda ws, error: print(error),
                 on_close = lambda ws: print("### closed ###"),
                 testnet: bool = False,
                 symbol: str = 'btcusdt', 
                 speed: str = '100ms'):
        '''
        
        To use TESTNET Binance Futures API  -> testnet = True
        
        To change currency pair             -> symbol = 'ethusdt'
        
        To change speed                     -> speed = '250ms'
        
        '''
        
        if testnet == True:
            self.wss_way = 'wss://fstream.binance.com/ws/'
        else:
            self.wss_way = 'wss://stream.binancefuture.com/ws/'
        
        self.interval = '1m'
        self.symbol = symbol.lower()
        self.speed = speed
        
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close


              
    def open_socket(self, way):
        websocket.enableTrace(False)
    
        self.ws = websocket.WebSocketApp(way,
                                    on_message=self.on_message,
                                    on_close=self.on_close,
                                    on_error=self.on_error)
        self.ws.run_forever()



    def aggregate_trade_socket(self):
        self.open_socket(f'{self.wss_way}{self.symbol}@aggTrade')



    def mark_price_socket(self):
        self.open_socket(f'{self.wss_way}{self.symbol}@markPrice')
        
        
        
    def candle_socket(self):
        self.open_socket(f'{self.wss_way}{self.symbol}@kline_{self.interval}')        
        

        
    def individual_symbol_mini_ticker(self):
        self.open_socket(f'{self.wss_way}{self.symbol}@miniTicker')
        
        
        
    def individual_symbol_ticker(self):
        self.open_socket(f'{self.wss_way}{self.symbol}@ticker')


    def all_book_ticker(self):
        self.open_socket(f'{self.wss_way}!bookTicker')
        
        
        
    def partial_book_depth_socket(self,
                                  levels: int = 20):
        '''
        To change count of top bids and asks -> levels = 5
        (5, 10 or 20 values are valid)
        '''
        self.open_socket(f'{self.wss_way}{self.symbol}@depth{levels}@{self.speed}')



    def diff_book_depth_socket(self):
        self.open_socket(f'{self.wss_way}{self.symbol}@depth@{self.speed}')



#%%



class Client:

    def __init__(self,
                 api_key: str,
                 sec_key: str,
                 testnet: bool = False,
                 symbol: str = 'BTCUSDT'):
        '''
        In any case you must give your API key and API secret to work with Client
        
        To use TESTNET Binance Futures API  -> testnet = True
        To change currency pair             -> symbol = 'ethusdt'
        '''
        
        self.api_key = api_key
        self.sec_key = sec_key
        self.http_way = 'http://fapi.binance.com/fapi/v1/'
        self.symbol = symbol
        self.X_MBX_APIKEY = {"X-MBX-APIKEY": self.api_key}
        
        if testnet == True:
            self.http_way = 'http://testnet.binancefuture.com/fapi/v1/'
            self.wss_way = 'wss://stream.binancefuture.com/ws/'
        else:
            self.http_way = 'http://fapi.binance.com/fapi/v1/'
            self.wss_way = 'wss://fstream.binance.com/ws/'
              
    def open_socket(self, way, on_message, on_error, on_close):
        websocket.enableTrace(False)
    
        self.ws = websocket.WebSocketApp(way,
                                    on_message=on_message, 
                                    on_error=on_error,
                                    on_close=on_close)
        self.ws.run_forever()


    def _get_request(self,
                      req,
                      query):
        r = requests.get(self.request_url(req=req, 
                                           query=query, 
                                           signature=self.get_sign(query=query)), 
                          headers=self.X_MBX_APIKEY)
        
        try:
            return r.json()
        except:
            if str(r) == '<Response [200]>':
                return dict([])
            else:
                return r
    
    def _post_request(self,
                      req,
                      query):
        r = requests.post(self.request_url(req=req, 
                                           query=query, 
                                           signature=self.get_sign(query=query)), 
                          headers=self.X_MBX_APIKEY)
        
        try:
            return r.json()
        except:
            if str(r) == '<Response [200]>':
                return dict([])
            else:
                return r
    
        
    def _delete_request(self,
                      req,
                      query):
        r = requests.delete(self.request_url(req=req, 
                                           query=query, 
                                           signature=self.get_sign(query=query)), 
                          headers=self.X_MBX_APIKEY)

        try:
            return r.json()
        except:
            if str(r) == '<Response [200]>':
                return dict([])
            else:
                return r
    
    
    def _put_request(self,
                      req,
                      query):
        r = requests.put(self.request_url(req=req, 
                                           query=query, 
                                           signature=self.get_sign(query=query)), 
                          headers=self.X_MBX_APIKEY)
        try:
            return r.json()
        except:
            if str(r) == '<Response [200]>':
                return dict([])
            else:
                return r





    @staticmethod
    def timestamp():        
        
        return int(time.time() * 1000)

    def get_sign(self, query):
        
        return hmac.new(self.sec_key.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()

    def request_url(self, req, query, signature):
        
        return self.http_way + req + query + '&signature=' + signature



    def new_order(self, 
                  side: str,
                  quantity: float,
                  price: float,
                  orderType: str = 'LIMIT',
                  timeInForce: str = 'GTC'):
        '''
        POST
        
        Choose side:                SELL or BUY
        Choose quantity:            0.001
        Choose price:               7500

        To change order type    ->  orderType = 'MARKET'
        To change time in force ->  timeInForce = 'IOC'
        '''
        req = 'order?'
        querystring = urllib.parse.urlencode({'symbol' : self.symbol, 
                                              'side' : side, 
                                              'type' : orderType, 
                                              'timeInForce' : timeInForce, 
                                              'quantity' : quantity, 
                                              'price' : price, 
                                              'timestamp' : self.timestamp()})

        return self._post_request(req, querystring)
        

    
    def query_order(self, orderId):
        '''
        GET
        
        Choose orderId: 156316486
        '''
        req = 'order?'
        querystring = urllib.parse.urlencode({'symbol' : self.symbol,
                                              'orderId' : orderId,
                                              'timestamp' : self.timestamp()})
    
        return self._get_request(req, querystring)



    def cancel_order(self, orderId):
        '''
        DELETE
        
        Choose orderId: 156316486
        '''
        req = 'order?'
        querystring = urllib.parse.urlencode({'symbol' : self.symbol,
                                              'orderId' : orderId,
                                              'timestamp' : self.timestamp()})

        return self._delete_request(req, querystring)



    def current_open_orders(self):
        '''
        GET
        '''
        req = 'openOrders?'
        querystring = urllib.parse.urlencode({'timestamp' : self.timestamp()})

        return self._get_request(req, querystring)



    def all_orders(self,
                   limit: int = 1000,
                   startTime: int = None,
                   endTime: int = None):
        '''
        GET

        To change limit of output orders    ->  limit = 1000
        (max value is 1000)
        To use start time and end time      ->  startTime = 1573661424937
                                            ->  endTime = 1573661428706
        '''
        req = 'allOrders?'
        querystring = urllib.parse.urlencode({'symbol' : self.symbol,
                                              'timestamp' : self.timestamp(),
                                              'limit' : limit, 
                                              'startTime' : startTime, 
                                              'endTime' : endTime})

        return self._get_request(req, querystring)



    def balance(self):
        '''
        GET
        '''
        req = 'balance?'
        querystring = urllib.parse.urlencode({'timestamp' : self.timestamp()})

        return self._get_request(req, querystring)



    def account_info(self):
        '''
        GET
        '''
        req = 'account?'
        querystring = urllib.parse.urlencode({'timestamp' : self.timestamp()})

        return self._get_request(req, querystring)



    def change_leverage(self, leverage):
        '''
        POST
        
        To change leverage -> leverage = 25
        (from 1 to 125 are valid values)
        '''
        req = 'leverage?'
        querystring = urllib.parse.urlencode({'symbol' : self.symbol,
                                              'leverage' : leverage,
                                              'timestamp' : self.timestamp()})

        return self._post_request(req, querystring)



    def position_info(self):
        '''GET'''
        req = 'positionRisk?'
        querystring = urllib.parse.urlencode({'timestamp' : self.timestamp()})
        
        return self._get_request(req, querystring)



    def trade_list(self,
                   limit: int = 1000,
                   startTime: int = None,
                   endTime: int = None):
        '''
        GET
        
        To change limit of output orders    -> limit = 1000
        (max value is 1000)
        To use start time and end time      -> startTime = 1573661424937
                                            -> endTime = 1573661428706
        '''
        req = 'userTrades?'
        querystring = urllib.parse.urlencode({'symbol' : self.symbol, 
                                              'timestamp' : self.timestamp(), 
                                              'limit' : limit, 
                                              'startTime' : startTime, 
                                              'endTime' : endTime})

        return self._get_request(req, querystring)



    def income_history(self,
                       limit: int = 1000):
        '''
        GET
        
        To change limit of output orders    -> limit = 1000
        (max value is 1000)
        '''
        req = 'income?'
        querystring = urllib.parse.urlencode({'symbol' : self.symbol,
                                              'timestamp' : self.timestamp(), 
                                              'limit' : limit})

        return self._get_request(req, querystring)



    def start_stream(self):
        '''
        POST
        '''
        req = 'listenKey?'
        querystring = urllib.parse.urlencode({'timestamp' : self.timestamp()})
        
        return self._post_request(req, querystring)
    
    def get_listen_key(self):
        return self.start_stream()['listenKey']

    def keepalive_stream(self):
        '''
        PUT
        '''
        req = 'listenKey?'
        querystring = urllib.parse.urlencode({'timestamp' : self.timestamp()})
        
        return self._put_request(req, querystring)

    def close_stream(self):
        '''
        DELETE
        '''
        req = 'listenKey?'
        querystring = urllib.parse.urlencode({'timestamp' : self.timestamp()})
        
        return self._delete_request(req, querystring)
    
    def user_update_socket(self, 
                           on_message, 
                           on_error, 
                           on_close):
        
        listen_key = self.get_listen_key()
        self.open_socket(f'{self.wss_way}{listen_key}', on_message, on_error, on_close)
        
    def stop_user_update_socket(self):
        self.close_stream()
