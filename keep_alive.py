from flask import Flask
from threading import Thread
import random
import time
import requests
import logging

app = Flask('')


@app.route('/')
def home():
    return "ok"


def run():
    app.run(host='0.0.0.0', port=6789)


def ping(target, debug):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    while (True):
        r = requests.get(target, headers=headers)
        if (debug == True):
            print("Status Code: " + str(r.status_code))
        time.sleep(random.randint(
            180, 300))  # alternate ping time between 3 and 5 minutes


def awake(target, debug=False):
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True
    t = Thread(target=run)
    r = Thread(target=ping, args=(
        target,
        debug,
    ))
    t.start()
    r.start()

# werkzeug
