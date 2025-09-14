"""Data processing module for gasoline price prediction.

This module provides functions to load historical gasoline price data,
perform basic cleaning, and generate features for modeling.
"""

import pandas as pd

def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load gasoline price data from a CSV file.

    Parameters
    ----------
    csv_path: str
        Path to the CSV file containing historical data.

    Returns
    -------
    pd.DataFrame
        DataFrame with the raw data.
    """
    return pd.read_csv(csv_path)

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the raw DataFrame.

    - Parse dates
    - Set date as index
    - Fill missing values
    - Create lag features

    Parameters
    ----------
    df: pd.DataFrame
        Raw data.

    Returns
    -------
    pd.DataFrame
        Processed data ready for modeling.
    """
    df = df.copy()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
    df = df.sort_index()
    df = df.fillna(method='ffill')
    # Example lag feature
    df['price_lag_1'] = df['price'].shift(1)
    df = df.dropna()
    return df