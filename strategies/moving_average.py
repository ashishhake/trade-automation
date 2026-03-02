import pandas as pd
from core.indicators import simple_moving_average


def moving_average_crossover(data: pd.DataFrame,
                             short_window: int = 3,
                             long_window: int = 5) -> pd.DataFrame:
    """
    Moving Average Crossover Strategy

    Parameters:
    data (pd.DataFrame): Market data with Close prices
    short_window (int): Short period moving average
    long_window (int): Long period moving average

    Returns:
    pd.DataFrame: Data with signals column (BUY/SELL)
    """

    # Create a copy so original data is not modified
    df = data.copy()

    # Calculate short and long moving averages
    df['SMA_Short'] = simple_moving_average(df, short_window)
    df['SMA_Long'] = simple_moving_average(df, long_window)

    # Create signal column (0 = no signal)
    df['Signal'] = 0.0

    # Generate BUY (1) and SELL (-1) signals
    df.loc[df['SMA_Short'] > df['SMA_Long'], 'Signal'] = 1
    df.loc[df['SMA_Short'] < df['SMA_Long'], 'Signal'] = -1

    return df
