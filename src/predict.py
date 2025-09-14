"""Prediction script for gasoline price forecasting.

This module ties together data loading, preprocessing, model training,
and visualization. It is intended to be run as a script or imported
by a notebook for interactive experimentation.
"""

from pathlib import Path
import pandas as pd

from .data_processing import load_data, preprocess
from .model import train_model, predict
from .visualization import plot_price_series, plot_predictions

def run_prediction(csv_path: Path, output_dir: Path):
    """
    Execute the full prediction pipeline.

    Parameters
    ----------
    csv_path : Path
        Path to CSV file containing historical gasoline price data.
    output_dir : Path
        Directory where any generated plots or artifacts will be saved.
    """
    # Load raw data
    raw_df = load_data(str(csv_path))

    # Preprocess and create features
    data_df = preprocess(raw_df)

    # Split into train and test (simple hold‑out split)
    split_idx = int(0.8 * len(data_df))
    train_df = data_df.iloc[:split_idx]
    test_df = data_df.iloc[split_idx:]

    # Train model
    model, train_rmse = train_model(train_df)

    # Predict on test set
    predictions = predict(model, test_df.drop(columns=["price"]))

    # Plot results
    plot_price_series(data_df, title="Historical Gasoline Prices")
    plot_predictions(test_df, predictions, title="Actual vs Predicted Prices")

    # Save plots (optional – matplotlib shows them interactively)
    # Users can modify this function to save figures to `output_dir`.

    print(f"Training RMSE: {train_rmse:.4f}")

if __name__ == "__main__":
    # Example usage – adjust paths as needed
    csv_file = Path("data/historical_gas_prices.csv")
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    run_prediction(csv_file, out_dir)