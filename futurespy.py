from sys import stdout
import time

import pandas as pd

import websocket
import requests
import urllib
import json


import hmac
import hashlib

import threading

"""
    That library have got just a part of Documentation
    If you want to know what does certain function use can find more on

    ! ! !
    https://binance-docs.github.io/apidocs/futures/en
    ! ! !
"""


class MarketData:
    def __init__(
        self,
        api_key=None,
        testnet: bool = False,
        symbol: str = "btcusdt",
        interval: str = "1m",
    ):

        """
        
        To use TESTNET Binance Futures API  -> testnet = True
        
        To change currency pair             -> symbol = 'ethusdt'
        
        To change interval                  -> interval = '5m'
        (m -> minutes
         h -> hours
         d -> days
         w -> weeks
         M -> months;
        
        Valid values: [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M])
        
        """

        if testnet == True:
            self.http_way = "http://testnet.binancefuture.com/fapi/v1/"
        else:
            self.http_way = "http://fapi.binance.com/fapi/v1/"

        self.wss_way = "wss://fstream.binance.com/ws/"
        self.interval = interval
        self.symbol = symbol.lower()
        self.api_key = api_key
        self.X_MBX_APIKEY = {"X-MBX-APIKEY": self.api_key}

    def ping(self):
        return requests.get(f"{self.http_way}ping").json()

    def server_time(self):
        return requests.get(f"{self.http_way}time").json()

    def exchange_info(self):
        return requests.get(f"{self.http_way}exchangeInfo").json()

    def order_book(self, limit: int = 100):
        """
        To change limit -> limit = 1000
        (Valid limits:[5, 10, 20, 50, 100, 500, 1000])
        """
        return requests.get(f"{self.http_way}depth?limit={limit}").json()

    def recent_trades(self, limit: int = 500):
        """
        To change limit -> limit = 1000
        (max 1000)
        """
        return requests.get(
            f"{self.http_way}trades?symbol={self.symbol}&limit={limit}"
        ).json()

    def historical_trades(self, limit: int = 500, fromId=None):
        """
        To change limit -> limit = 1000
        (max 1000)
        """
        if fromId:
            return requests.get(
                f"{self.http_way}historicalTrades?symbol={self.symbol}&limit={limit}&fromId={fromId}",
                headers=self.X_MBX_APIKEY,
            ).json()
        else:
            return requests.get(
                f"{self.http_way}historicalTrades?symbol={self.symbol}&limit={limit}",
                headers=self.X_MBX_APIKEY,
            ).json()

    def aggregate_trades(
        self,
        fromId: int = None,
        startTime: int = None,
        endTime: int = None,
        limit: int = 500,
    ):
        """
        To change limit                     ->  limit = 1000
        (max 1000)
        
        To use fromId                       ->  fromId = 1231
        To use start time and end time      ->  startTime = 1573661424937
                                            ->  endTime = 1573661428706
        """
        return requests.get(
            f"{self.http_way}aggTrades?symbol={self.symbol}&fromId={fromId}&startTime={startTime}&endTime={endTime}&limit={limit}"
        ).json()

    def mark_price(self):
        return requests.get(f"{self.http_way}premiumIndex?symbol={self.symbol}").json()

    def funding_rate(
        self, startTime: int = None, endTime: int = None, limit: int = 100
    ):
        """
        To change limit                     ->  limit = 1000
        (max 1096)
        
        To use start time and end time      ->  startTime = 1573661424937
                                            ->  endTime = 1573661428706
        """
        return requests.get(
            f"{self.http_way}klines?symbol={self.symbol}&startTime={startTime}&endTime={endTime}&limit={limit}"
        ).json()

    def ticker_price_24h(self, symbol: bool = False):
        if symbol is True:
            return requests.get(
                f"{self.http_way}ticker/24hr?symbol={self.symbol}"
            ).json()
        else:
            return requests.get(f"{self.http_way}ticker/24hr").json()

    def ticker_price_symbol(self, symbol: bool = False):
        if symbol is True:
            return requests.get(
                f"{self.http_way}ticker/price?symbol={self.symbol}"
            ).json()
        else:
            return requests.get(f"{self.http_way}ticker/price").json()

    def ticker_orderbook_symbol(self, symbol: bool = False):
        if symbol is True:
            return requests.get(
                f"{self.http_way}ticker/bookTicker?symbol={self.symbol}"
            ).json()
        else:
            return requests.get(f"{self.http_way}ticker/bookTicker").json()

    def candles_data(
        self,
        interval: str = "1m",
        startTime: int = None,
        endTime: int = None,
        limit: int = 500,
    ):
        """
        To change interval                  ->  interval = '5m'
        (Valid values: [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M])
        
        To use limit                        ->  limit = 1231
        (Default 500; max 1500)
        
        To use start time and end time      ->  startTime = 1573661424937
                                            ->  endTime = 1573661428706
        """
        return requests.get(
            f"{self.http_way}klines?symbol={self.symbol}&interval={interval}&startTime={startTime}&endTime={endTime}&limit={limit}"
        ).json()

    def load_last_candles(self, days=30, on_update=None):
        """
        DEPRESIATED
        Use load_historical_candles instead
        """
        limit = 1440

        one_hour_in_milliseconds = 3600000
        one_day_in_milliseconds = one_hour_in_milliseconds * 24

        startTime = int(round(time.time() * 1000)) - (
            one_day_in_milliseconds * days
        )  # 30 days = 30, 90 days = 90

        data = []

        for k in range(days):
            r = requests.get(
                f"{self.http_way}klines?symbol={self.symbol}&interval={self.interval}&limit={limit}&starttime={startTime}"
            )
            startTime += one_day_in_milliseconds
            response = r.json()

            if on_update is not None:
                on_update(int(100 * (k / days)))

            for i in range(len(response)):
                data.append(response[i])

        """
        last_req = requests.get(f"{self.http_way}klines?symbol={self.symbol}&interval={self.interval}&limit=1")
        last_res = last_req.json()
        last_res = last_res[0]
        
        if last_res[0] != data[-1][0]:
            print("New candle added!")

            data.append(last_res)
            del data[0]
        """

        df = pd.DataFrame(data)
        df = df.iloc[:, :6]
        df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

        df["Date"] = pd.to_datetime(df["Date"], unit="ms")
        df["Date"] = df["Date"].map(lambda x: x.strftime("%Y-%m-%d %H:%M"))

        df = df.astype(
            {
                "Open": "float64",
                "High": "float64",
                "Low": "float64",
                "Close": "float64",
                "Volume": "float64",
            }
        )

        return df

    def load_historical_candles(
        self, count: int = 30000, on_update=None
    ) -> pd.DataFrame:
        tm = int(round(time.time() * 1000))

        lim = []
        if count == 1500:
            lim.append(count)
        else:
            lim.append(count % 1500)
        while count > 1500:
            lim.append(1500)
            count -= 1500

        for i in range(len(lim)):
            if lim[i] == 0:
                lim[i] = 1500

        tmp_list = []
        for i, j in enumerate(reversed(lim)):
            tmp = self.candles_data(interval=self.interval, limit=j, endTime=tm)

            if on_update is not None:
                on_update(int(100 * ((i + 1) / len(lim))))

            if type(tmp) != list:
                print(tmp, i)
            for candle in reversed(tmp):
                dd = {
                    "Date": candle[0],
                    "Open": float(candle[1]),
                    "High": float(candle[2]),
                    "Low": float(candle[3]),
                    "Close": float(candle[4]),
                    "Volume": float(candle[5]),
                }
                tmp_list.append(dd)
            if len(tmp) not in lim:
                print("--- Not enough data ---")
                return
            tm = tmp[0][0] - 1

        df = pd.DataFrame(reversed(tmp_list))
        df["Date"] = pd.to_datetime(df["Date"], unit="ms")
        df["Date"] = df["Date"].map(lambda x: x.strftime("%Y-%m-%d %H:%M"))

        return df


#%%


class WebsocketMarket:
    def __init__(
        self,
        on_message=lambda ws, message: print(message),
        on_error=lambda ws, error: print(error),
        on_close=lambda ws: print("### closed ###"),
        testnet: bool = False,
        symbol: str = "btcusdt",
        interval: str = "1m",
        speed: str = "100ms",
    ):
        """
        
        To use TESTNET Binance Futures API  -> testnet = True
        
        To change currency pair             -> symbol = 'ethusdt'
        
        To change speed                     -> speed = '250ms'
        
        """

        if testnet == True:
            self.wss_way = "wss://stream.binancefuture.com/ws/"
        else:
            self.wss_way = "wss://fstream.binance.com/ws/"

        self.interval = interval
        self.symbol = symbol.lower()
        self.speed = speed

        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close

    @staticmethod
    def parced(func):
        def parced_func(ws, msg):
            return func(ws, json.loads(msg))

        return parced_func

    def open_socket(self, way):
        thread = threading.Thread(target=lambda: self._open_socket(way))
        thread.start()

    def _open_socket(self, way):
        websocket.enableTrace(False)

        on_message_with_parce = WebsocketMarket.parced(self.on_message)
        self.ws = websocket.WebSocketApp(
            way,
            on_message=on_message_with_parce,
            on_close=self.on_close,
            on_error=self.on_error,
        )
        self.ws.run_forever()

    def aggregate_trade_socket(self):
        self.open_socket(f"{self.wss_way}{self.symbol}@aggTrade")

    def mark_price_socket(self):
        self.open_socket(f"{self.wss_way}{self.symbol}@markPrice")

    def candle_socket(self):
        self.open_socket(f"{self.wss_way}{self.symbol}@kline_{self.interval}")

    def individual_symbol_mini_ticker(self):
        self.open_socket(f"{self.wss_way}{self.symbol}@miniTicker")

    def individual_symbol_ticker(self):
        self.open_socket(f"{self.wss_way}{self.symbol}@ticker")

    def all_book_ticker(self):
        self.open_socket(f"{self.wss_way}!bookTicker")

    def partial_book_depth_socket(self, levels: int = 20):
        """
        To change count of top bids and asks -> levels = 5
        (5, 10 or 20 values are valid)
        """
        self.open_socket(f"{self.wss_way}{self.symbol}@depth{levels}@{self.speed}")

    def diff_book_depth_socket(self):
        self.open_socket(f"{self.wss_way}{self.symbol}@depth@{self.speed}")


#%%


class Client:
    def __init__(
        self,
        api_key: str,
        sec_key: str,
        testnet: bool = False,
        symbol: str = "BTCUSDT",
        recv_window: int = 30000,
    ):
        """
        In any case you must give your API key and API secret to work with Client
        
        To use TESTNET Binance Futures API  -> testnet = True
        To change currency pair             -> symbol = 'ethusdt'
        """

        self.api_key = api_key
        self.sec_key = sec_key
        self.http_way = "http://fapi.binance.com/fapi/v1/"
        self.symbol = symbol
        self.X_MBX_APIKEY = {"X-MBX-APIKEY": self.api_key}

        self.recvWindow = recv_window

        if testnet == True:
            self.http_way = "http://testnet.binancefuture.com/fapi/v1/"
            self.wss_way = "wss://stream.binancefuture.com/ws/"
        else:
            self.http_way = "http://fapi.binance.com/fapi/v1/"
            self.wss_way = "wss://fstream.binance.com/ws/"

    def server_time(self):
        try:
            return requests.get(f"{self.http_way}time").json()
        except Exception as e:
            self.logger.error(e)
            return None

    def open_socket(self, way, on_message, on_error, on_close):
        self.thread = threading.Thread(
            target=lambda: self._open_socket(way, on_message, on_error, on_close)
        )
        self.thread.start()

    def _open_socket(self, way, on_message, on_error, on_close):
        try:
            websocket.enableTrace(False)

            self.ws = websocket.WebSocketApp(
                way, on_message=on_message, on_error=on_error, on_close=on_close
            )
            self.ws.run_forever()
        except Exception as e:
            self.logger.error(e)

    def _get_request(self, req, query):
        r = requests.get(
            self.request_url(
                req=req, query=query, signature=self.get_sign(query=query)
            ),
            headers=self.X_MBX_APIKEY,
        )

        try:
            return r.json()
        except:
            if str(r) == "<Response [200]>":
                return dict([])
            else:
                return r

    def _post_request(self, req, query):
        r = requests.post(
            self.request_url(
                req=req, query=query, signature=self.get_sign(query=query)
            ),
            headers=self.X_MBX_APIKEY,
        )

        try:
            return r.json()
        except:
            if str(r) == "<Response [200]>":
                return dict([])
            else:
                return r

    def _delete_request(self, req, query):
        r = requests.delete(
            self.request_url(
                req=req, query=query, signature=self.get_sign(query=query)
            ),
            headers=self.X_MBX_APIKEY,
        )

        try:
            return r.json()
        except:
            if str(r) == "<Response [200]>":
                return dict([])
            else:
                return r

    def _put_request(self, req, query):
        r = requests.put(
            self.request_url(
                req=req, query=query, signature=self.get_sign(query=query)
            ),
            headers=self.X_MBX_APIKEY,
        )
        try:
            return r.json()
        except:
            if str(r) == "<Response [200]>":
                return dict([])
            else:
                return r

    def check_keys(self):
        response = self.balance()
        return (
            True
            if isinstance(response, list)
            else False
            if isinstance(response, dict)
            and "code" in response
            and response["code"] == -2014
            else response["msg"]
            if isinstance(response, dict) and "msg" in response
            else str(response)
        )

    def timestamp(self, server: bool = False):
        if server:
            server_time = self.server_time()["serverTime"]
            return (
                server_time if server_time is not None else self.timestamp(server=False)
            )
        else:
            return int(time.time() * 1000)

    def get_sign(self, query):

        return hmac.new(
            self.sec_key.encode("utf-8"), query.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def request_url(self, req, query, signature):

        return self.http_way + req + query + "&signature=" + signature

    def new_order(
        self,
        symbol: str,
        side: str,
        orderType: str,
        quantity: float,
        timeInForce: float = None,
        reduceOnly: bool = False,
        price: float = None,
        newClientOrderId: str = None,
        stopPrice: float = None,
        workingType: str = None,
    ):
        """
        POST
        
        Choose side:                SELL or BUY
        Choose quantity:            0.001
        Choose price:               7500

        To change order type    ->  orderType = 'MARKET'
        To change time in force ->  timeInForce = 'IOC'
        """

        req = "order?"

        querystring = {
            "symbol": symbol,
            "side": side,
            "type": orderType,
            "quantity": quantity,
            "reduceOnly": reduceOnly,
        }
        if timeInForce is not None:
            querystring["timeInForce"] = timeInForce
        if price is not None:
            querystring["price"] = price
        if newClientOrderId is not None:
            querystring["newClientOrderId"] = newClientOrderId
        if stopPrice is not None:
            querystring["stopPrice"] = stopPrice
        if workingType is not None:
            querystring["workingType"] = workingType
        querystring["timestamp"] = self.timestamp()
        querystring["recvWindow"] = self.recvWindow

        querystring = urllib.parse.urlencode(querystring)

        return self._post_request(req, querystring)
    
    def place_multiple_orders(self, orders_list):
        """
        POST
        """
        req = "batchOrders?"
        querystring = urllib.parse.urlencode(
            {
                "batchOrders": orders_list,
                "recvWindow": self.recvWindow,
                "timestamp": self.timestamp(),
            }
        )
        querystring = querystring.replace('%27', '%22')
        
        return self._post_request(req, querystring)

    def query_order(self, symbol: str, orderId, clientID=False):
        """
        GET
        
        Choose orderId: 156316486
        """
        req = "order?"
        querystring = urllib.parse.urlencode(
            {
                "symbol": symbol,
                "orderId" if not clientID else "origClientOrderId": orderId,
                "recvWindow": self.recvWindow,
                "timestamp": self.timestamp(),
            }
        )

        return self._get_request(req, querystring)

    def cancel_order(self, symbol: str, orderId, clientID=False):
        """
        DELETE
        
        Choose orderId: 156316486
        """
        req = "order?"
        querystring = urllib.parse.urlencode(
            {
                "symbol": symbol,
                "orderId" if not clientID else "origClientOrderId": orderId,
                "recvWindow": self.recvWindow,
                "timestamp": self.timestamp(),
            }
        )

        return self._delete_request(req, querystring)

    def cancel_all_open_orders(self, symbol: str):
        """
        DELETE
        """
        req = "allOpenOrders?"
        querystring = urllib.parse.urlencode(
            {
                "symbol": symbol,
                "recvWindow": self.recvWindow,
                "timestamp": self.timestamp(),
            }
        )

        return self._delete_request(req, querystring)

    def cancel_multiple_orders(self, symbol: str, orderIdList):
        """
        DELETE
        
        List of orderIds (max: 10)
        """
        req = "batchOrders?"
        querystring = urllib.parse.urlencode(
            {
                "symbol": symbol,
                "orderIdList": orderIdList,
                "recvWindow": self.recvWindow,
                "timestamp": self.timestamp(),
            }
        )

        return self._delete_request(req, querystring)

    def current_open_orders(self):
        """
        GET
        """
        req = "openOrders?"
        querystring = urllib.parse.urlencode(
            {"recvWindow": self.recvWindow, "timestamp": self.timestamp()}
        )

        return self._get_request(req, querystring)

    def all_orders(self, limit: int = 1000, startTime: int = None, endTime: int = None):
        """
        GET

        To change limit of output orders    ->  limit = 1000
        (max value is 1000)
        To use start time and end time      ->  startTime = 1573661424937
                                            ->  endTime = 1573661428706
        """
        req = "allOrders?"
        querystring = urllib.parse.urlencode(
            {
                "symbol": self.symbol,
                "limit": limit,
                "startTime": startTime,
                "endTime": endTime,
                "recvWindow": self.recvWindow,
                "timestamp": self.timestamp(),
            }
        )

        return self._get_request(req, querystring)

    def balance(self):
        """
        GET
        """
        req = "balance?"
        querystring = urllib.parse.urlencode(
            {"recvWindow": self.recvWindow, "timestamp": self.timestamp()}
        )

        return self._get_request(req, querystring)

    def account_info(self):
        """
        GET
        """
        req = "account?"
        querystring = urllib.parse.urlencode(
            {"recvWindow": self.recvWindow, "timestamp": self.timestamp()}
        )

        return self._get_request(req, querystring)

    def change_leverage(self, leverage):
        """
        POST
        
        To change leverage -> leverage = 25
        (from 1 to 125 are valid values)
        """
        req = "leverage?"
        querystring = urllib.parse.urlencode(
            {
                "symbol": self.symbol,
                "leverage": leverage,
                "recvWindow": self.recvWindow,
                "timestamp": self.timestamp(),
            }
        )

        return self._post_request(req, querystring)

    def position_info(self):
        """GET"""
        req = "positionRisk?"
        querystring = urllib.parse.urlencode(
            {"recvWindow": self.recvWindow, "timestamp": self.timestamp()}
        )

        return self._get_request(req, querystring)

    def trade_list(self, limit: int = 1000, startTime: int = None, endTime: int = None):
        """
        GET
        
        To change limit of output orders    -> limit = 1000
        (max value is 1000)
        To use start time and end time      -> startTime = 1573661424937
                                            -> endTime = 1573661428706
        """
        req = "userTrades?"
        querystring = urllib.parse.urlencode(
            {
                "symbol": self.symbol,
                "limit": limit,
                "startTime": startTime,
                "endTime": endTime,
                "recvWindow": self.recvWindow,
                "timestamp": self.timestamp(),
            }
        )

        return self._get_request(req, querystring)

    def income_history(self, limit: int = 1000):
        """
        GET
        
        To change limit of output orders    -> limit = 1000
        (max value is 1000)
        """
        req = "income?"
        querystring = urllib.parse.urlencode(
            {
                "symbol": self.symbol,
                "recvWindow": self.recvWindow,
                "limit": limit,
                "timestamp": self.timestamp(),
            }
        )

        return self._get_request(req, querystring)

    def start_stream(self):
        """
        POST
        """
        req = "listenKey?"
        querystring = urllib.parse.urlencode(
            {"recvWindow": self.recvWindow, "timestamp": self.timestamp()}
        )

        return self._post_request(req, querystring)

    def get_listen_key(self):
        return self.start_stream()["listenKey"]

    def keepalive_stream(self):
        """
        PUT
        """
        req = "listenKey?"
        querystring = urllib.parse.urlencode(
            {"recvWindow": self.recvWindow, "timestamp": self.timestamp()}
        )

        return self._put_request(req, querystring)

    def close_stream(self):
        """
        DELETE
        """
        req = "listenKey?"
        querystring = urllib.parse.urlencode(
            {"recvWindow": self.recvWindow, "timestamp": self.timestamp()}
        )

        return self._delete_request(req, querystring)

    def user_update_socket(
        self,
        on_message=lambda ws, message: (
            stdout.write(f"\r{json.loads(message)}"),
            print(),
        ),
        on_error=lambda ws, error: print(error),
        on_close=lambda ws: print("### closed ###"),
    ):

        listen_key = self.get_listen_key()
        self.open_socket(f"{self.wss_way}{listen_key}", on_message, on_error, on_close)

    def stop_user_update_socket(self):
        self.close_stream()
