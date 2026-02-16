import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Download stock data
# Ticker: "RELIANCE.NS" (NSE Reliance)
# Period: 6 months of daily data
data = yf.download("HCLTECH.NS", period="1y", interval="1d")

# 2. Calculate Moving Averages
# MA_20: Short-term (20-day) moving average
# MA_50: Long-term (50-day) moving average
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()

# 3. Generate Buy/Sell Signals
buy_signals = []
sell_signals = []
position = False  # To track if we are in a "buy" position

for i in range(len(data)):
    ma20 = data['MA20'].iloc[i]
    ma50 = data['MA50'].iloc[i]

    if pd.isna(ma20) or pd.isna(ma50):
        buy_signals.append(None)
        sell_signals.append(None)
        continue

    if ma20 > ma50 and not position:
        buy_signals.append(data['Close'].iloc[i])
        sell_signals.append(None)
        position = True
    
    elif ma20 < ma50 and position:
        buy_signals.append(None)
        sell_signals.append(data['Close'].iloc[i])
        position = False

    else:
        buy_signals.append(None)
        sell_signals.append(None)


data['Buy_Signal'] = buy_signals
data['Sell_Signal'] = sell_signals

# 4. Plotting
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label="Close Price", alpha=0.5)
plt.plot(data['MA20'], label="MA 20", color='blue', linewidth=1.5)
plt.plot(data['MA50'], label="MA 50", color='orange', linewidth=1.5)

# Plot Buy signals
plt.scatter(data.index, data['Buy_Signal'], label='Buy', marker='^', color='green', s=100)

# Plot Sell signals
plt.scatter(data.index, data['Sell_Signal'], label='Sell', marker='v', color='red', s=100)

plt.title("HCLTECH Moving Average Buy/Sell Strategy")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()
