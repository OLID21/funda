import requests
import datetime
import pytz
import telegram
import time

# Telegram Bot Details
TELEGRAM_BOT_TOKEN = "7625611810:AAE8zOPSI3Znfbxwi52oQEcPVu3y84uNYbU"
TELEGRAM_CHAT_ID = "7863258597"

# Funda Search URL - (Might require manual investigation of how Funda structures search queries)
FUNDA_URL = "https://www.funda.nl/en/koop/utrecht/0-3800-euro-per-m2/"

# Function to fetch and parse listings
def get_funda_listings():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(FUNDA_URL, headers=headers)
    
    if response.status_code != 200:
        return []

    # Process data - this step will vary based on Funda's website structure
    listings = []  # Parse listings from HTML/JSON
    # (You'll need to inspect Funda's structure using dev tools)
    
    return listings

# Function to filter new listings from the last 24 hours
def filter_new_listings(listings):
    one_day_ago = datetime.datetime.now(pytz.timezone("CET")) - datetime.timedelta(days=1)
    
    new_listings = [
        listing for listing in listings
        if listing["date_listed"] >= one_day_ago
        and listing["price_per_m2"] <= 3800
    ]
    
    return new_listings

# Function to send Telegram message
def send_telegram_message(message):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Main function
def main():
    listings = get_funda_listings()
    new_listings = filter_new_listings(listings)

    if new_listings:
        message = f"New Funda Listings in Utrecht:\n"
        for listing in new_listings:
            message += f"\n🏡 {listing['title']} - {listing['price_per_m2']} €/m²"
            message += f"\n🔗 {listing['url']}\n"
        
        send_telegram_message(message)
    else:
        send_telegram_message("No new listings found today.")

# Run script at 16:00 CET daily
while True:
    now = datetime.datetime.now(pytz.timezone("CET"))
    
    if now.hour == 16 and now.minute == 0:
        main()
        time.sleep(60)  # Prevent multiple triggers in the same minute

