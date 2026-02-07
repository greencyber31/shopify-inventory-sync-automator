import shopify
import os
from dotenv import load_dotenv

load_dotenv()

# Setup session
# Note: Using SHOPIFY_ACCESS_TOKEN as defined in .env
session = shopify.Session(os.getenv('SHOP_URL'), '2024-01', os.getenv('SHOPIFY_ACCESS_TOKEN'))
shopify.ShopifyResource.activate_session(session)

# Fetch locations
try:
    locations = shopify.Location.find()
    with open('locations.txt', 'w') as f:
        f.write(f"Found {len(locations)} locations:\n")
        for loc in locations:
            line = f"Location Name: {loc.name} | ID: {loc.id}\n"
            f.write(line)
            print(line) # Keep print just in case
except Exception as e:
    with open('locations.txt', 'w') as f:
        f.write(f"Error fetching locations: {e}\n")
    print(f"Error fetching locations: {e}")
