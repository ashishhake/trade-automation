import pandas as pd


def apply_risk_management(data: pd.DataFrame, risk_per_trade: float = 0.1) -> pd.DataFrame:
    """
    Apply basic risk management to trading signals.
    """

    # Create a proper copy (safe)
    df = data.copy()

    # Initialize position size column
    df['Position_Size'] = 0.0

    for i in range(len(df)):
        signal = float(df.iloc[i]['Signal'])


        # BUY signal → allocate fraction of capital
        if signal == 1:
            df.loc[df.index[i], 'Position_Size'] = risk_per_trade

        # SELL signal → close position
        elif signal == -1:
            df.loc[df.index[i], 'Position_Size'] = 0.0

        # HOLD → carry previous position
        else:
            if i > 0:
                prev_size = df.iloc[i - 1]['Position_Size']
                df.loc[df.index[i], 'Position_Size'] = prev_size

    return df
