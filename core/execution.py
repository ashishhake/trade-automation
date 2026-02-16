import pandas as pd


def execute_trades(data: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate trade execution based on signals.

    Parameters:
    data (pd.DataFrame): Data containing Signal and Close price

    Returns:
    pd.DataFrame: Data with trade execution details
    """

    # Copy data to avoid modifying original
    df = data.copy()

    # Track current position (0 = no trade, 1 = in trade)
    position = 0

    # Create new columns
    df['Trade'] = "HOLD"
    df['Entry_Price'] = 0.0
    df['Exit_Price'] = 0.0

    for i in range(len(df)):
        signal = df['Signal'].iloc[i]
        price = df['Close'].iloc[i]

        # If BUY signal and no open position
        if signal == 1 and position == 0:
            position = 1
            df['Trade'].iloc[i] = "BUY"
            df['Entry_Price'].iloc[i] = price

        # If SELL signal and position is open
        elif signal == -1 and position == 1:
            position = 0
            df['Trade'].iloc[i] = "SELL"
            df['Exit_Price'].iloc[i] = price

        else:
            df['Trade'].iloc[i] = "HOLD"

    return df
