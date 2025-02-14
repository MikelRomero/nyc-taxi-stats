import argparse
from datetime import datetime
import json
import os
from data_loader import download_parquet, load_data
from metrics import compute_metrics
from utils import generate_output_filename, save_json
from config import OUTPUT_DIR

def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Compute NYC Yellow Taxi KPIs.")
    parser.add_argument("--date", type=str, required=True, help="Target date (YYYY-MM-DD)")
    return parser.parse_args()

def main():
    args = parse_args()
    target_date = datetime.strptime(args.date, "%Y-%m-%d")
    
    # Generate the output filename using the target date
    filename = generate_output_filename(target_date)
    output_filepath = os.path.join(OUTPUT_DIR, filename)
    # Check if the file already exists
    if os.path.isfile(output_filepath):
        print(f"File for {target_date.strftime('%Y-%m-%d')} already exists: {output_filepath}")
        
        # Read the existing JSON file and return the data
        with open(output_filepath, 'r') as f:
            metrics = json.load(f)
        print("Returning existing metrics.")
        print(json.dumps(metrics, indent=4))
    else:
        # Load and process data
        df = load_data(target_date)
        metrics = compute_metrics(df)

        # Save results
        filename = generate_output_filename(target_date)
        save_json(metrics, OUTPUT_DIR, filename)
        print(f"Metrics saved to {OUTPUT_DIR}/{filename}")


if __name__ == "__main__":
    main()