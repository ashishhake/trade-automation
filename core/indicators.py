import pandas as pd


def simple_moving_average(data: pd.DataFrame, window: int) -> pd.Series:
    """
    Calculate Simple Moving Average (SMA)

    Parameters:
    data (pd.DataFrame): Market data containing 'Close' prices
    window (int): Number of periods for moving average (e.g., 5, 10, 20)

    Returns:
    pd.Series: SMA values
    """

    # Check if 'Close' column exists
    if 'Close' not in data.columns:
        raise ValueError("Data must contain a 'Close' column")

    # Calculate Simple Moving Average using pandas rolling mean
    sma = data['Close'].rolling(window=window).mean()

    return sma
