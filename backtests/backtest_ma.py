import pandas as pd


def backtest_strategy(data: pd.DataFrame, initial_capital: float = 10000) -> pd.DataFrame:
    """
    Simple Backtesting Engine for Moving Average Strategy
    """

    df = data.copy()

    cash = initial_capital
    shares = 0
    portfolio_values = []

    for i in range(len(df)):
        signal = df.iloc[i]['Signal']
        price = df.iloc[i]['Close']

        # BUY condition
        if signal == 1 and shares == 0:
            shares = cash / price
            cash = 0

        # SELL condition
        elif signal == -1 and shares > 0:
            cash = shares * price
            shares = 0

        # Portfolio value calculation
        portfolio_value = cash + (shares * price)
        portfolio_values.append(portfolio_value)

    df['Portfolio_Value'] = portfolio_values

    return df
