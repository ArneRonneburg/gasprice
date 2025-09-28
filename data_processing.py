import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import logging
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
with open('config.yaml') as f:
    config = yaml.safe_load(f)

JET_STATION_UUID = config['station_uuid']
DEFAULT_INPUT = config['data_paths']['raw']
DEFAULT_OUTPUT = config['data_paths']['processed']

# Data validation schema
SCHEMA = {
    'date': 'datetime64[ns]',
    'station_uuid': 'object',
    'e5': 'float64',
    'e10': 'float64',
    'diesel': 'float64'
}

def load_raw_data(input_dir):
    """Load and validate raw CSV files"""
    files = list(Path(input_dir).glob('*.csv'))
    if not files:
        raise FileNotFoundError(f'No CSV files in {input_dir}')
    
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f, parse_dates=['date'], dtype={'station_uuid': str})
            # Schema validation
            assert all(df[col].dtype == dtype for col, dtype in SCHEMA.items())
            dfs.append(df)
            logger.info(f'Successfully loaded {f.name}')
        except Exception as e:
            logger.error(f'Skipped {f.name}: {str(e)}')
    
    return pd.concat(dfs)

# ... [rest of processing functions from previous implementation] ...

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--input', default=DEFAULT_INPUT)
        parser.add_argument('--output', default=DEFAULT_OUTPUT)
        args = parser.parse_args()
        
        logger.info(f'Starting data processing from {args.input}')
        raw_df = load_raw_data(args.input)
        
        logger.info('Processing data...')
        processed_df = process_gas_data(raw_df)
        
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        processed_df.to_csv(args.output, index=False)
        logger.info(f'Data saved to {args.output}')
        
    except Exception as e:
        logger.exception('Data processing failed')
        raise
