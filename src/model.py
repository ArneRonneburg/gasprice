"""Model module for gasoline price prediction.

This module defines a simple regression model using scikit‑learn.
It includes functions to train the model and to make predictions.
"""

from typing import Tuple
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def train_model(train_df: pd.DataFrame) -> Tuple[LinearRegression, float]:
    """
    Train a LinearRegression model.

    Parameters
    ----------
    train_df : pd.DataFrame
        Training data with a ``price`` column as the target and
        any number of feature columns.

    Returns
    -------
    model : LinearRegression
        Trained regression model.
    rmse : float
        Root‑mean‑square error on the training set.
    """
    X = train_df.drop(columns=["price"])
    y = train_df["price"]
    model = LinearRegression()
    model.fit(X, y)
    predictions = model.predict(X)
    rmse = mean_squared_error(y, predictions, squared=False)
    return model, rmse

def predict(model, input_df: pd.DataFrame) -> pd.Series:
    """
    Generate predictions using a trained model.

    Parameters
    ----------
    model : LinearRegression
        Trained model returned by :func:`train_model`.
    input_df : pd.DataFrame
        DataFrame containing the same feature columns used for training.

    Returns
    -------
    pd.Series
        Predicted gasoline prices.
    """
    return pd.Series(model.predict(input_df), index=input_df.index)