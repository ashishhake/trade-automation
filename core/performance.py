import pandas as pd
import numpy as np


def calculate_performance(data: pd.DataFrame) -> dict:
    """
    Calculate performance metrics for the trading strategy.
    """

    df = data.copy()

    # 1️⃣ Total Return
    initial_value = df['Portfolio_Value'].iloc[0]
    final_value = df['Portfolio_Value'].iloc[-1]
    total_return = (final_value / initial_value - 1) * 100

    # 2️⃣ Daily Returns
    df['Daily_Return'] = df['Portfolio_Value'].pct_change()

    # Remove first NaN
    daily_returns = df['Daily_Return'].dropna()

    # 3️⃣ Sharpe Ratio (Assuming 252 trading days)
    sharpe_ratio = 0
    if daily_returns.std() != 0:
        sharpe_ratio = (
            daily_returns.mean() / daily_returns.std()
        ) * np.sqrt(252)

    # 4️⃣ Max Drawdown
    cumulative_max = df['Portfolio_Value'].cummax()
    drawdown = (df['Portfolio_Value'] - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min() * 100

    return {
        "Total Return (%)": round(total_return, 2),
        "Sharpe Ratio": round(sharpe_ratio, 2),
        "Max Drawdown (%)": round(max_drawdown, 2)
    }