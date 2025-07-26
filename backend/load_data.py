import os
import pandas as pd
from pymongo import MongoClient

# --- Config ---
DATA_FOLDER = '../data'
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecommerce"

csv_to_collection = {
    'distribution_centers.csv': 'distribution_centers',
    'inventory_items.csv': 'inventory_items',
    'order_items.csv': 'order_items',
    'orders.csv': 'orders',
    'products.csv': 'products',
    'users.csv': 'users'
}

# --- Connect to MongoDB ---
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

for csv_filename, collection_name in csv_to_collection.items():
    csv_path = os.path.join(DATA_FOLDER, csv_filename)
    print(f"\nLoading {csv_path} into collection `{collection_name}` ...")
    df = pd.read_csv(csv_path)
    records = df.to_dict(orient='records')

    # Optional: Clear collection before inserting (remove if you want to append instead)
    db[collection_name].delete_many({})

    # Bulk insert
    if records:
        db[collection_name].insert_many(records)
        print(f"Inserted {len(records)} documents into `{collection_name}`.")
    else:
        print(f"Skipping `{collection_name}`: CSV is empty.")

print("\nAll CSVs loaded into MongoDB!")
