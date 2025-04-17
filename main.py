from flask import Flask
import threading
import time
import requests

app = Flask(__name__)

ETSY_API_KEY = "5vmy5xamvjm33xy66epxht08"
SHOP_NAME = "JPWoodsandPrints"  # Replace this if you didn't already
SMIIRL_URL = "https://api.smiirl.com/40cb5aa8a1d491413edc730a1098ea65"

def get_sales():
    url = f"https://openapi.etsy.com/v2/shops/{SHOP_NAME}?api_key={ETSY_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["results"][0]["transaction_sold_count"]
    else:
        print("Failed to get data from Etsy:", response.status_code, response.text)
        return None

def update_counter(sales):
    payload = {"number": sales}
    response = requests.post(SMIIRL_URL, json=payload)
    if response.status_code == 200:
        print(f"Counter updated to {sales}")
    else:
        print("Failed to update counter:", response.status_code, response.text)

def background_loop():
    while True:
        sales = get_sales()
        if sales is not None:
            update_counter(sales)
        time.sleep(600)

# Start background thread
threading.Thread(target=background_loop, daemon=True).start()

@app.route('/')
def home():
    return "Etsy-Smiirl Sync is running!"

@app.route('/ping')
def ping():
    return "pong"
