import pandas as pd


def backtest_strategy(data: pd.DataFrame, initial_capital: float = 10000) -> pd.DataFrame:
    """
    Simple Backtesting Engine for Moving Average Strategy

    Parameters:
    data (pd.DataFrame): Data with Close price and Signal column
    initial_capital (float): Starting money for simulation

    Returns:
    pd.DataFrame: Data with portfolio performance
    """

    # Create a copy of the data
    df = data.copy()

    # Position: 1 = holding stock, 0 = no stock
    df['Position'] = 0

    # Portfolio value tracking
    cash = initial_capital
    shares = 0
    portfolio_values = []

    for index, row in df.iterrows():
        signal = row['Signal']
        price = row['Close']

        # BUY condition
        if signal == 1 and shares == 0:
            shares = cash / price  # buy with full capital
            cash = 0

        # SELL condition
        elif signal == -1 and shares > 0:
            cash = shares * price  # sell all shares
            shares = 0

        # Calculate total portfolio value
        portfolio_value = cash + (shares * price)
        portfolio_values.append(portfolio_value)

    # Add portfolio value to dataframe
    df['Portfolio_Value'] = portfolio_values

    return df
