import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from datetime import datetime, timedelta, timezone
from typing import Optional
from config import PARQUET_URL_TEMPLATE, DATA_DIR, RELEVANT_COLUMNS

def download_parquet(year: int, month: int) -> str:
    """Downloads official NYC TLC Parquet files if they don't exist locally."""
    # Construct download URL from template
    url = PARQUET_URL_TEMPLATE.format(year=year, month=month)
    filename = url.split("/")[-1]
    file_path = os.path.join(DATA_DIR, filename)
    
    # Download if file doesn't exist
    if not os.path.exists(file_path):
        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"Downloading {filename}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(response.content)
        except Exception as e:
            # Cleanup partial downloads on error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise RuntimeError(f"Download failed for {filename}: {str(e)}")
    
    return file_path

def load_data(target_date):
    # Define explicit schema for critical columns
    schema = pa.schema([
        ("tpep_pickup_datetime", pa.timestamp("ms")),  # Unix timestamp in milliseconds
        ("tpep_dropoff_datetime", pa.timestamp("ms")), # Unix timestamp in milliseconds
        ("trip_distance", pa.float32()),       # 32-bit float sufficient for distance
        ("total_amount", pa.float32()),        # Optimized for monetary values
        ("payment_type", pa.int8()),           # Small integer type (1-6)
        ("tip_amount", pa.float32()),
        ("extra", pa.float32())
    ])
    
    try:
        # Download or locate Parquet file
        file_path = download_parquet(target_date.year, target_date.month)
        
        # Define start and end timestamps for filtering
        start_ts = target_date
        end_ts = target_date + timedelta(days=1)
          # Convert to milliseconds
        
        print(f"Filtering data from {start_ts} to {end_ts}")
        
        # Read with Arrow-native filtering
        table = pq.read_table(
            file_path,
            schema=schema,
            filters=[
                ("tpep_pickup_datetime", ">=", start_ts),
                ("tpep_pickup_datetime", "<", end_ts)
            ],
            columns=RELEVANT_COLUMNS
        )
        
        # Convert to Pandas with memory-optimized types
        df = table.to_pandas()
        
        # Convert Unix timestamps to datetime
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], unit='ms', utc=True)
        #df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], unit='ms', utc=True)
        
        if not df.empty:
            min_date = df['tpep_pickup_datetime'].min()
            max_date = df['tpep_pickup_datetime'].max()
            print(f"Rango de datos cargados: {min_date} - {max_date}")
        
        return df

    except Exception as e:
        print(f"Error en carga de datos: {type(e).__name__} - {str(e)}")
        return pd.DataFrame()