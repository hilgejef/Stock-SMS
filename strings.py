### A repository of long strings to use within the SMS/stock-ticker app.
#! May reintegrate into flask_app.py

# Called when sending (SYMBOL) ... response
symbol_response = "{symbol}: {price}"

# Called when sending (SYMBOL) MORE INFO response
expanded_response = \
"""
{symbol},
Last Trade Price: {last_trade_price},
Today's Opening: {opening_price},
Previous Closing: {closing_price},
Today's High: {price_high},
Today's Low: {price_low},
Last Trade Time: {last_trade_time}
"""

# Called when sending (SYMBOL) SUBSCRIBE response
subscription_response = "You've been subscribed to daily stock alerts for {symbol}"

# Called when (SYMBOL) SUBSCRIBE returns preexisting tracker
already_subscribed = "You are already subscribed to daily stock alerts for {symbol}"

# Called when sending (SYMBOL) UNSUBSCRIBE response
unsubscribed = "You have been successfuly unsubscribed from alerts for {symbol}"

# Called when (SYMBOL) UNSUBSCRIBE returns no existing tracker
not_subscribed = "You were not previously subscribed to alerts for {symbol}"

# Called when accessing MySQL database from flask_app
db_uri_string = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"