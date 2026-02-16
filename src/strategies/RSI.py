import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


data = yf.download("ADANIPOWER.NS", start="2025-01-01", end="2025-02-01", interval="1d")

# print(data)

def calculate_rsi(series, period=14):
    series = series.squeeze()
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    
    gain = pd.Series(gain, index=series.index)
    loss = pd.Series(loss, index=series.index)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


data['RSI'] = calculate_rsi(data['Close'])
print(data[['Close', 'RSI']])

