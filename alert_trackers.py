# alert_trackers.py
# This script queries the database for all trackers and sends expanded
# stock information for each PHONE#, SYMBOL pair

import os
from credentials import Twilio_Credentials
from urlparse import urlparse
from twilio.rest import TwilioRestClient
from twilio.rest.resources import Connection
from twilio.rest.resources.connection import PROXY_TYPE_HTTP
from stock_sms import Tracker, db
from strings import tracker_alert
from request_stock_info import get_all_symbol

# Initialization of Twilio Client
client = TwilioRestClient(Twilio_Credentials.sid, Twilio_Credentials.token)

# Proxy initialization
# See: https://www.pythonanywhere.com/forums/topic/3854/
proxy_url = os.environ.get("http_proxy")
host, port = urlparse(proxy_url).netloc.split(":")
Connection.set_proxy_info(host, int(port), proxy_type=PROXY_TYPE_HTTP)

# Find unique symbols, make Yahoo Finance API call for each symbol,
# send expanded info to each phone number subscribed to that symbol
for symbol_tuple in db.session.query(Tracker.symbol).distinct().all():
    symbol = symbol_tuple[0]
    info = get_all_symbol(symbol)

    for tracker in Tracker.query.filter_by(symbol=symbol).all():
        body = tracker_alert.format(symbol=symbol,
                                    last_trade_price=info["last_trade_price"],
                                    opening_price=info["today_open"],
                                    closing_price=info["previous_close"],
                                    price_high=info["todays_high"],
                                    price_low=info["todays_low"],
                                    last_trade_time=["last_trade_time"])

        client.messages.create(to=tracker.phone_number,
                              from_=Twilio_Credentials.phone_number,
                              body=body)
