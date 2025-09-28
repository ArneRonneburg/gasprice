import pandas as pd
import numpy as np
from pathlib import Path
import argparse

# Configuration
JET_STATION_UUID = '474e5046-deaf-4f9b-9a32-2d8a1b0ae8ab'
DEFAULT_INPUT = '/root/tankerkoenig-data/data'
DEFAULT_OUTPUT = 'data/processed_prices.csv'

# 1. Data loader
def load_raw_data(input_dir):
    files = list(Path(input_dir).glob('*.csv'))
    if not files:
        raise FileNotFoundError(f'No CSV files in {input_dir}')
    
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, parse_dates=['date'], dtype={'station_uuid': str})
            dfs.append(df)
        except Exception as e:
            print(f'Skipped {f.name}: {e}')
    return pd.concat(dfs)

# 2. Processing pipeline
def process_gas_data(df):
    # Filter target station
    station_df = df[df['station_uuid'] == JET_STATION_UUID].copy()
    
    # Time-based processing
    station_df = station_df.sort_values('date').set_index('date')
    resampled = station_df.resample('5T').asfreq()
    
    # Handle missing values
    for fuel in ['e5', 'e10', 'diesel']:
        resampled[fuel] = resampled[fuel].interpolate(method='time', limit=6)
    
    # Feature engineering
    resampled['hour'] = resampled.index.hour
    resampled['day_of_week'] = resampled.index.dayofweek
    resampled['is_weekend'] = resampled['day_of_week'].isin([5,6]).astype(int)
    
    return resampled.reset_index()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=DEFAULT_INPUT)
    parser.add_argument('--output', default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    
    print('Loading data from:', args.input)
    raw_df = load_raw_data(args.input)
    
    print('Processing data...')
    processed_df = process_gas_data(raw_df)
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(args.output, index=False)
    print(f'Saved processed data to {args.output}')
