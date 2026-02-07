# Shopify Inventory Sync Automator 📦🚀

## 📝 Overview
This is a professional Python-based automation tool designed for Shopify store owners and Technical Virtual Assistants. It solves the common problem of syncing warehouse/supplier CSV data with Shopify by dynamically mapping human-readable SKUs to Shopify's internal Inventory Item IDs.

**Key Problem Solved:** Manual data entry for inventory is slow and prone to errors. This script automates the process using the Shopify API, ensuring stock levels are always accurate.

---

## ✨ Key Features
* **Dynamic SKU Mapping:** Automatically fetches current product data from Shopify to match SKUs—no manual ID searching required.
* **Bulk Inventory Updates:** Syncs quantity levels across specific Shopify locations in seconds.
* **Data Validation:** Uses **Pandas** to process CSV data and identifies missing SKUs before attempting updates.
* **Secure & Professional:** Utilizes `.env` files for credential security and includes error handling for API rate limits.
* **Detailed Logging:** Generates a success/fail report after every sync for audit trails.

---

## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **Libraries:** `pandas`, `shopify-python-api`, `python-dotenv`
* **Environment:** Developed on SteamOS (Linux) using Distrobox.

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/greencyber31/shopify-inventory-sync-automator.git](https://github.com/greencyber31/shopify-inventory-sync-automator.git)
   cd shopify-inventory-sync-automator