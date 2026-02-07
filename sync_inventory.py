import shopify
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json

# 1. Load credentials
load_dotenv()

ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
# Clean the URL just in case the user added https://
raw_url = os.getenv("SHOP_URL", "").replace("https://", "").replace("http://", "").strip()
STORE_URL = raw_url
API_VERSION = os.getenv("API_VERSION", "2024-01")

if not ACCESS_TOKEN or not STORE_URL:
    print("Error: Missing SHOPIFY_ACCESS_TOKEN or SHOP_URL in .env file.")
    exit(1)

# Initialize Shopify Session for GraphQL lookup (keeping previous handy logic)
session = shopify.Session(STORE_URL, API_VERSION, ACCESS_TOKEN)
shopify.ShopifyResource.activate_session(session)

def get_inventory_item_id_by_sku(sku):
    """
    Finds the inventory_item_id for a given SKU using Shopify GraphQL API.
    """
    query = f'''
    {{
      productVariants(first: 1, query: "sku:{sku}") {{
        edges {{
          node {{
            inventoryItem {{
              id
            }}
          }}
        }}
      }}
    }}
    '''
    try:
        response = shopify.GraphQL().execute(query)
        data = json.loads(response)
        edges = data.get('data', {}).get('productVariants', {}).get('edges', [])
        if edges:
            # ID looks like gid://shopify/InventoryItem/123456789
            gid = edges[0]['node']['inventoryItem']['id']
            return gid.split('/')[-1]
    except Exception as e:
        print(f"Error looking up SKU {sku}: {e}")
    
    return None

def update_shopify_inventory(inventory_item_id, location_id, new_quantity):
    """
    Updates the inventory level for a specific item at a specific location using shopify.InventoryLevel.set().
    """
    try:
        shopify.InventoryLevel.set(location_id, inventory_item_id, int(new_quantity))
        return True
    except Exception as e:
        print(f"   -> API Request Error: {e}")
        return False

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    csv_file = "supplier_inventory.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        exit(1)

    print(f"Reading {csv_file}...")
    try:
        df = pd.read_csv(csv_file)
        
        # Verify columns exist
        required_cols = ['sku', 'quantity', 'location_id']
        # Normalize headers to lowercase for easier matching
        df.columns = [c.lower() for c in df.columns]
        
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"Error: Missing columns in CSV: {missing}")
            print(f"Found columns: {list(df.columns)}")
            exit(1)

        print(f"Found {len(df)} rows. Starting sync...")
        
        results = []
        from datetime import datetime

        for index, row in df.iterrows():
            sku = str(row['sku']).strip()
            quantity = row['quantity']
            location_id = row['location_id'] # Make sure this is in your CSV!
            
            status = "Failed" # Default
            
            try:
                # Step 1: Map SKU to Inventory ID
                inventory_id = get_inventory_item_id_by_sku(sku)
                
                if inventory_id:
                    # Step 2: Update Inventory
                    success = update_shopify_inventory(inventory_id, location_id, quantity)
                    
                    if success:
                        print(f"Updated SKU {sku} to {quantity}")
                        status = "Success"
                    else:
                        print(f"Failed to update SKU {sku}")
                        status = "Failed"
                else:
                    print(f"SKU {sku} not found in Shopify.")
                    status = "Not Found"
            
            except Exception as e:
                print(f"Error processing row {index+1} (SKU: {row.get('sku', 'UNKNOWN')}): {e}")
                status = f"Error: {e}"
            
            results.append({
                "sku": sku,
                "status": status,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        # Save results
        results_df = pd.DataFrame(results)
        output_file = "sync_results.csv"
        results_df.to_csv(output_file, index=False)
        print(f"\nSync complete. Results saved to {output_file}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
