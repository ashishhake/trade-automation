import pandas as pd


def apply_risk_management(data: pd.DataFrame, risk_per_trade: float = 0.1) -> pd.DataFrame:
    """
    Apply basic risk management to trading signals.

    Parameters:
    data (pd.DataFrame): Data containing Signal and Close price
    risk_per_trade (float): Fraction of capital to risk per trade (e.g., 0.1 = 10%)

    Returns:
    pd.DataFrame: Data with position size column
    """

    # Create a copy to avoid modifying original data
    df = data.copy()

    # Initialize position size column
    df['Position_Size'] = 0.0

    for i in range(len(df)):
        signal = df['Signal'].iloc[i]

        # If BUY signal, allocate only a fraction of capital
        if signal == 1:
            df['Position_Size'].iloc[i] = risk_per_trade

        # If SELL signal, close position
        elif signal == -1:
            df['Position_Size'].iloc[i] = 0.0

        else:
            # Hold previous position size (no new trade)
            if i > 0:
                df['Position_Size'].iloc[i] = df['Position_Size'].iloc[i - 1]

    return df
