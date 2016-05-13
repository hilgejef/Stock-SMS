# alert_trackers.py
# This script queries the database for all trackers and sends expanded
# stock information for each PHONE#, SYMBOL pair

import os
import ystockquote
from credentials import Twilio_Credentials
from urlparse import urlparse
from twilio.rest import TwilioRestClient
from twilio.rest.resources import Connection
from twilio.rest.resources.connection import PROXY_TYPE_HTTP
from flask_app import Tracker
from strings import tracker_alert

# Initialization of Twilio Client
client = TwilioRestClient(Twilio_Credentials.sid, Twilio_Credentials.token)

# Proxy initialization
# See: https://www.pythonanywhere.com/forums/topic/3854/
proxy_url = os.environ.get("http_proxy")
host, port = urlparse(proxy_url).netloc.split(":")
Connection.set_proxy_info(host, int(port), proxy_type=PROXY_TYPE_HTTP)

# Get trackers and send expanded reponse for each
for tracker in Tracker.query.all():
    to = tracker.phone_number
    symbol = tracker.symbol

    body = tracker_alert.format(
                    symbol=symbol,
                    last_trade_price=ystockquote.get_last_trade_price(symbol),
                    opening_price=ystockquote.get_today_open(symbol),
                    closing_price=ystockquote.get_previous_close(symbol),
                    price_high=ystockquote.get_todays_high(symbol),
                    price_low=ystockquote.get_todays_low(symbol),
                    last_trade_time=ystockquote.get_last_trade_time(symbol)
                )

    client.messages.create(to=to, from_=Twilio_Credentials.phone_number, body=body)
