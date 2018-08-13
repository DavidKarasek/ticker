import websocket
import ssl
import asyncio
import json
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from dotenv import load_dotenv
import os

#load env variables for flask secret key
load_dotenv()

class ExchangeListener():
    url = ""
    exchange = ""

    def __init__(self, exchange, url):
        self.url = url
        self.exchange = exchange

    def on_message(self, ws, message):
        print("--> {} message <--".format(self.exchange))
        socketio.emit('tick', {'exchange':self.exchange, 'data': ticker, 'type': 'ticker'}, namespace='/ticker')

    def on_error(self, ws, error):
        print("--> {} Error! <--".format(self.exchange))
        print(error)

    def on_close(self, ws):
        print("--> {} closed <--".format(self.exchange))

    def on_open(self, ws):
        print("--> {} connection opened <--".format(self.exchange))

    def connect(self):
        # exit if nothing to connect to
        if self.url == "": return
        
        ws = websocket.WebSocketApp(self.url, 
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        ws.on_open = self.on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

class Hitbtc(ExchangeListener):

    url = "wss://api.hitbtc.com/api/2/ws"
    exchange = "hitbtc"

    def __init__(self):
        print("Initializing {}".format(self.exchange))

    def on_open(self, ws):
        print("--> {} override open <--".format(self.exchange))
        ws.send(json.dumps({"method":"subscribeTicker","params":{"symbol": "LTCBTC"}, "id": 1011}))

    def on_message(self, ws, message):
        print("--> {} override message <--".format(self.exchange))
        msg = json.loads(message)
        ticker = {
            "time": msg["params"]["timestamp"],
            "best_ask": msg["params"]["ask"],
            "best_bid": msg["params"]["bid"],
            "last_trade": msg["params"]["last"]
        }
        socketio.emit('tick', {'exchange':self.exchange, 'data': ticker, 'type': 'ticker'}, namespace='/ticker')

class Bitfinex(ExchangeListener):

    url = "wss://api.bitfinex.com/ws/2"
    exchange = "bitfinex"

    def __init__(self):
        print("Initializing {}".format(self.exchange))

    def on_open(self, ws):
        print("--> {} override open <--".format(self.exchange))
        ws.send(json.dumps({"event":"subscribe","channel": "ticker", "symbol": "tLTCBTC"}))

    def on_message(self, ws, message):
        print("--> {} override message <--".format(self.exchange))
        msg = json.loads(message)
        now = datetime.now().timestamp()*1000

        # determine message type
        if len(msg[1]) == 2:
            # heart beat
            print("Heart beat")
        elif len(msg[1]) == 10:
            # ticker stream
            ticker = {
                "time": now,
                "best_ask": msg[1][0],
                "best_bid": msg[1][2],
                "last_trade": msg[1][6]
            }
            socketio.emit('tick', {'exchange':self.exchange, 'data': ticker, 'type': 'ticker'}, namespace='/ticker')

# setup flask server to host app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET")
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/ticker')
def test_connect():
    emit('tick', {'data': 'Connected'})

if __name__ == "__main__":

    # create hitbtc instance
    hitbtc = Hitbtc()
    hitbtcThread = Thread(target=hitbtc.connect)
    hitbtcThread.start()

    # create bitfinex instance
    bitfinex = Bitfinex()
    bitfinexThread = Thread(target=bitfinex.connect)
    bitfinexThread.start()

    socketio.run(app)