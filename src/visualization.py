"""Visualization module for gasoline price prediction.

Provides simple plotting utilities using matplotlib to visualize
historical prices and model predictions.
"""

import matplotlib.pyplot as plt
import pandas as pd

def plot_price_series(df: pd.DataFrame, title: str = "Gasoline Price Over Time"):
    """
    Plot a time series of gasoline prices.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with a DateTime index and a ``price`` column.
    title : str, optional
        Plot title.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["price"], label="Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_predictions(actual: pd.DataFrame, predicted: pd.Series, title: str = "Actual vs Predicted"):
    """
    Plot actual vs. predicted gasoline prices.

    Parameters
    ----------
    actual : pd.DataFrame
        DataFrame containing the true ``price`` column.
    predicted : pd.Series
        Predicted price series with the same index as ``actual``.
    title : str, optional
        Plot title.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(actual.index, actual["price"], label="Actual")
    plt.plot(predicted.index, predicted, label="Predicted", linestyle="--")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()