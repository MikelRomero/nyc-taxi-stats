import json
import os
from datetime import datetime
import numpy as np

def convert_to_native_types(data):
    """Convert numpy data types to native Python types."""
    if isinstance(data, dict):
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_native_types(v) for v in data]
    elif isinstance(data, np.generic):
        return data.item()
    else:
        return data

def generate_output_filename(date: datetime) -> str:
    """Generate JSON filename."""
    return f"{date.strftime('%Y%m%d')}_yellow_taxi_kpis.json"

def save_json(data: dict, output_dir: str, filename: str) -> None:
    """Save metrics to JSON."""
    os.makedirs(output_dir, exist_ok=True)
    data = convert_to_native_types(data)  # Convert numpy types to native types
    with open(os.path.join(output_dir, filename), 'w') as f:
        json.dump(data, f, indent=2)