import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download Data
data = yf.download("HDFCBANK.NS", period="1y", interval="1d", auto_adjust=True)

# Calculate Moving Averages
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()

# Vectorized signal logic
data['Signal'] = 0
data['Signal'] = (data['MA20'] > data['MA50']).astype(int)
data['Position'] = data['Signal'].diff()  # 1 = buy, -1 = sell

# Plot
plt.figure(figsize=(14,7))
plt.plot(data['Close'], label="Close Price", alpha=0.5)
plt.plot(data['MA20'], label="MA 20", color='blue')
plt.plot(data['MA50'], label="MA 50", color='orange')

# Buy signals
plt.scatter(data.index[data['Position'] == 1], 
            data['Close'][data['Position'] == 1], 
            label='Buy', marker='^', color='green', s=100)

# Sell signals
plt.scatter(data.index[data['Position'] == -1], 
            data['Close'][data['Position'] == -1], 
            label='Sell', marker='v', color='red', s=100)

plt.title("HDFCBANK Moving Average Buy/Sell Strategy")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()
