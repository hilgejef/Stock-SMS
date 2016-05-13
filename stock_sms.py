# Stock-SMS -- Jeffrey Hilger
# Stock-SMS is an application that allows users to send SMS commands to
# a predesignated phone number, and receive realtime stock ticker information
# as SMS replies.

import os
import strings
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from twilio import twiml
from urlparse import urlparse
from twilio.rest.resources import Connection
from twilio.rest.resources.connection import PROXY_TYPE_HTTP
from credentials import DB_Credentials
from request_stock_info import get_all_symbol
from ystockquote import get_last_trade_price


### BASIC APP INITIALIZATIONS

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = strings.db_uri_string.format(
        username=DB_Credentials.user,
        password=DB_Credentials.pw,
        hostname="Hilger.mysql.pythonanywhere-services.com",
        databasename="Hilger$db",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

@app.before_first_request
def set_proxy():
    # Free PythonAnywhere accounts are blocked from external IP access,
    # except through proxy whitelist
    # See: https://www.pythonanywhere.com/forums/topic/3854/
    proxy_url = os.environ.get("http_proxy")
    host, port = urlparse(proxy_url).netloc.split(":")
    Connection.set_proxy_info(host, int(port), proxy_type=PROXY_TYPE_HTTP)


### MODELS

# The Tracker model describes a table in which Phone#, Stock Symbol are
# both primary keys, and is used to track subscriptions to stock updates
class Tracker(db.Model):
    __tablename__ = "Trackers"

    phone_number = db.Column(db.String(16), primary_key=True)
    symbol = db.Column(db.String(16), primary_key=True)

    def __init__(self, phone_number, symbol):
        self.phone_number = phone_number
        self.symbol = symbol

    def __repr__(self):
        return "{phone_number}: {symbol}".format(
            phone_number=self.phone_number,
            symbol=self.symbol
        )


### VIEWS

@app.route('/', methods=["POST"])
def sms_response():
    # Twilio SMS data is received as a form, and the form's data is accessed
    # via various attributes ("Body" for message body, etc.)
    from_ = request.form["From"]
    incoming = request.form["Body"].upper().split()

    # The Twilio response object allows return messages to be sent
    resp = twiml.Response()

    # Determine the request type and respond accordingly
    # (SYMBOL) "SUBSCRIBE" -> Add (SYMBOL, PHONE#) to the database.
    if len(incoming) == 2 and incoming[1] == "SUBSCRIBE":
        symbol = incoming[0]

        tracker = Tracker.query.filter_by(phone_number=from_, symbol=symbol).first()

        # Check for preexisting tracker before attempting add, respond
        # accordingly
        if not tracker:
            db.session.add(Tracker(phone_number=from_, symbol=symbol))
            db.session.commit()

            resp.message(strings.subscription_response.format(symbol=symbol))

        else:
            resp.message(strings.already_subscribed.format(symbol=symbol))

    # (SYMBOL) "UNSUBSCRIBE" -> Remove (SYMBOL, PHONE#) from the database
    elif len(incoming) == 2 and incoming[1] == "UNSUBSCRIBE":
        symbol = incoming[0]

        tracker = Tracker.query.filter_by(phone_number=from_, symbol=symbol).first()

        # Check for preexisting tracker before attempting delete, respond
        # accordingly
        if not tracker:
            resp.message(strings.not_subscribed.format(symbol=symbol))
        else:
            db.session.delete(tracker)
            db.session.commit()

            resp.message(strings.unsubscribed.format(symbol=symbol))

    # (SYMBOL) ... "EXPAND" -> Send expanded (SYMBOL) information for each symbol
    elif incoming[-1] == "EXPAND":
        for symbol in incoming[:-1]:

            info = get_all_symbol(symbol)

            outgoing = strings.expanded_response.format(
                        symbol=symbol,
                        last_trade_price=info["last_trade_price"],
                        opening_price=info["today_open"],
                        closing_price=info["previous_close"],
                        price_high=info["todays_high"],
                        price_low=info["todays_low"],
                        last_trade_time=info["last_trade_time"]
                    )

            resp.message(outgoing)

    # (SYMBOL) ... -> Send (SYMBOL) stock price for each symbol
    # Symbols should be white-space delimited (e.g. SYMBOL SYMBOL ...)
    else:
        outgoing = []

        # Build list of stock prices and join as newline delimited string
        for symbol in incoming:
            price = get_last_trade_price(symbol)
            outgoing.append(strings.symbol_response.format(symbol=symbol, price=price))

        resp.message(",\n".join(outgoing))

    return str(resp)




