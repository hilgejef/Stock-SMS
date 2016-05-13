# Stock-SMS

#### Purpose

Stock-SMS is an application that allows users to send commands via SMS and receive realtime stock ticker information.


#### Technologies

Stock-SMS leverages Python/Flask, Twilio, Yahoo Finance via the ystockquote Python package, MySQL and PythonAnywhere.

#### Usage

To use Stock-SMS, send one of these specific commands to a predesignated phone number. Keep in mind that (SYMBOL) indicates a valid stock ticker symbol (GOOG, YHOO, etc).

- SYMBOL SYMBOL (...): Any number of whitespace delimited stock ticker symbols will return last trade price for each symbol.
- SYMBOL EXPAND: A stock ticker symbol followed by "expand" will return additional trading details for that symbol.
- SYMBOL SUBSCRIBE: A stock ticker symbol followed by "subscribe" will subscribe the associated phone number to a daily trading report for that symbol.
- SYMBOL UNSUBSCRIBE: A stock ticker symbol followed by "unsubscribe" will unsubscribe the associated phone number from the daily trading report for that symbol.
