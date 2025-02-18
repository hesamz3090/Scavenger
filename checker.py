import sqlite3
from lib.perpetual import Perpetual
import numpy as np

access_id = ""  # Replace with your access id
secret_key = ""  # Replace with your secret key

market = 'TRXUSDT'

# Initialize database
conn = sqlite3.connect("sqlite.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id TEXT,
        market TEXT,
        market_pressure REAL,
        current_price REAL,
        median_asks REAL,
        median_bids REAL,
        total_asks REAL,
        total_bids REAL,
        max_ask_volume REAL,
        max_bid_volume REAL,
        trade_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

client = Perpetual(access_id, secret_key)
position = client.get_position(market)
trade_id = None
trade_type = None

if position['message'] == 'OK' and position['data']:
    trade_id = position['data'][0]['position_id']  # Assuming the first trade is active
    trade_type = position['data'][0]['side']  # Assuming side gives 'long' or 'short'

data = client.get_depth(market, '0.001')
asks = data['data']['depth']['asks']
bids = data['data']['depth']['bids']

asks_volumes = [float(x[1]) for x in asks]
bids_volumes = [float(x[1]) for x in bids]

median_asks_volume = np.median(asks_volumes)
median_bids_volume = np.median(bids_volumes)

asks_volume_sum = sum(asks_volumes)
bids_volume_sum = sum(bids_volumes)
market_pressure = (bids_volume_sum / (bids_volume_sum + asks_volume_sum)) * 100

now_price = float(client.get_price(market)['data'][0]['price'])
asks_max_volume = max(asks_volumes)
bids_max_volume = max(bids_volumes)

# Insert data into SQLite
db_data = (trade_id, market, market_pressure, now_price, median_asks_volume, median_bids_volume, asks_volume_sum, bids_volume_sum, asks_max_volume, bids_max_volume, trade_type)
cursor.execute('''
    INSERT INTO info (trade_id, market, market_pressure, current_price, median_asks, median_bids, total_asks, total_bids, max_ask_volume, max_bid_volume, trade_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', db_data)
conn.commit()

print("Data stored successfully")

# Close connection
conn.close()