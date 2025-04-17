import requests
import time

ETSY_API_KEY = "5vmy5xamvjm33xy66epxht08"  # This is pending, full access may require OAuth later
SHOP_NAME = "JPWoodsandPrints"  # Replace with your Etsy shop name
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

# Run every 10 minutes
while True:
    sales = get_sales()
    if sales is not None:
        update_counter(sales)
    time.sleep(120)  # 600 seconds = 10 minutes
