from datetime import datetime
import os

# URLs and paths
PARQUET_URL_TEMPLATE = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
DATA_DIR = os.getenv("DATA_DIR", "data")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# Relevant columns
RELEVANT_COLUMNS = [
    'tpep_pickup_datetime',
    'total_amount',
    'trip_distance',
    'payment_type',
    'tip_amount',
    'extra'
]