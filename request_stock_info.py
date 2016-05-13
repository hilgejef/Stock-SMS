from ystockquote import _request

# Request tokens
last_trade_price = "l1"
today_open = "o"
prev_close = "p"
todays_high = "h"
todays_low = "g"
last_trade_time = "t1"

ids = "".join([last_trade_price, today_open,
                  prev_close, todays_high, todays_low, last_trade_time])

def get_all_symbol(symbol):
    values = _request(symbol, ids).split(",")

    return dict(last_trade_price=values[0],
                today_open=values[1],
                previous_close=values[2],
                todays_high=values[3],
                todays_low=values[4],
                last_trade_time=values[5])