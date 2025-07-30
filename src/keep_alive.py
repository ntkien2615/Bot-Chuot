from flask import Flask, jsonify
from threading import Thread
import random
import time
import requests
import logging
import os

# Disable Flask logging completely
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True

app = Flask('')
app.logger.disabled = True
app.logger.setLevel(logging.ERROR)

@app.route('/')
def home():
    """Ultra minimal health check endpoint"""
    return "OK"

@app.route('/health')
def health():
    """Minimal health check"""
    return jsonify({"status": "up"})

@app.route('/ping')
def ping_endpoint():
    """Minimal ping endpoint"""
    return "pong"


def run():
    """Run Flask app with minimal logging"""
    # Disable all Flask logs
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)


def ping(target, debug):
    """Ping the target URL to keep service alive"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    while True:
        try:
            r = requests.get(f"{target}/ping", headers=headers, timeout=10)
            if debug:
                print(f"✅ Ping successful: {r.status_code}")
        except Exception as e:
            if debug:
                print(f"❌ Ping failed: {e}")
        
        # Sleep between 3-5 minutes
        time.sleep(random.randint(180, 300))


def awake(target, debug=False):
    """Start the keep-alive service with minimal logging"""
    # Completely disable werkzeug logging
    logging.getLogger('werkzeug').disabled = True
    app.logger.disabled = True
    
    # Only enable debug if explicitly requested and not in production
    debug_mode = debug and os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    # Start Flask server thread
    t = Thread(target=run, daemon=True)
    
    # Start ping thread only if target provided
    if target:
        r = Thread(target=ping, args=(target, debug_mode), daemon=True)
        r.start()
    
    t.start()
    
    if debug_mode:
        print(f"🚀 Keep-alive service started on port 8080")
        if target:
            print(f"🔄 Pinging {target} every 3-5 minutes")
