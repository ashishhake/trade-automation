import pandas as pd


def execute_trades(data: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate trade execution based on signals.
    """

    df = data.copy()

    position = 0  # 0 = no trade, 1 = in trade

    df['Trade'] = "HOLD"
    df['Entry_Price'] = 0.0
    df['Exit_Price'] = 0.0

    for i in range(len(df)):
        signal = df.iloc[i]['Signal']
        price = df.iloc[i]['Close']

        # BUY
        if signal == 1 and position == 0:
            position = 1
            df.loc[df.index[i], 'Trade'] = "BUY"
            df.loc[df.index[i], 'Entry_Price'] = price

        # SELL
        elif signal == -1 and position == 1:
            position = 0
            df.loc[df.index[i], 'Trade'] = "SELL"
            df.loc[df.index[i], 'Exit_Price'] = price

        else:
            df.loc[df.index[i], 'Trade'] = "HOLD"

    return df
