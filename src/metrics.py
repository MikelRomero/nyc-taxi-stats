import pandas as pd

def compute_metrics(df: pd.DataFrame) -> dict:
    """Compute all required KPIs."""
    if df.empty:
        return {}
    
    # 1. Average price per mile
    total_amount = df['total_amount'].sum()
    total_distance = df['trip_distance'].sum()
    avg_price_per_mile = total_amount / total_distance if total_distance > 0 else 0.0
    
    # 2. Payment type distribution
    payment_dist = df['payment_type'].value_counts().astype(int).to_dict()
    
    # 3. Custom indicator
    valid_rows = df[df['trip_distance'] > 0]
    custom_indicator = (
        (valid_rows['tip_amount'] + valid_rows['extra']) / valid_rows['trip_distance']
    ).mean()
    
    return {
        "average_price_per_mile": round(avg_price_per_mile, 2),
        "payment_type_distribution": {str(k): int(v) for k, v in payment_dist.items()},
        "custom_indicator": round(custom_indicator, 2)
    }