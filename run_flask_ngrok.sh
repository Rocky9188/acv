#!/bin/bash

# Flask অ্যাপ চালানো
python app.py &

# ngrok দিয়ে টানেল খোলা
sleep 2
termux-open-url http://127.0.0.1:4040
ngrok http 5000
