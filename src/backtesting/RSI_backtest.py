import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Download Data
data = yf.download("ADANIPOWER.NS", period="1d", interval="1m")

# --- RSI Function ---
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

# Calculate RSI
data['RSI'] = calculate_rsi(data['Close'])

# --- Trading Rules ---
buy_level = 40
sell_level = 60

trades = []
buy_price = None

for i in range(len(data)):
    if data['RSI'].iloc[i] < buy_level and buy_price is None:  # Buy condition
        buy_price = float(data['Close'].iloc[i])

    elif data['RSI'].iloc[i] > sell_level and buy_price is not None:  # Sell condition
        sell_price = float(data['Close'].iloc[i])
        profit = sell_price - buy_price
        trades.append(profit)
        buy_price = None  # reset

# --- Results ---
results = pd.DataFrame({'Profit_per_Trade': trades})
results['Cumulative_Profit'] = results['Profit_per_Trade'].cumsum()

total_trades = len(results)
winning_trades = (results['Profit_per_Trade'] > 0).sum()
losing_trades = (results['Profit_per_Trade'] <= 0).sum()
win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
total_profit = results['Profit_per_Trade'].sum()

print("📊 RSI Strategy Backtest Results")
print(f"Total Trades: {total_trades}")
print(f"Winning Trades: {winning_trades}")
print(f"Losing Trades: {losing_trades}")
print(f"Win Rate: {win_rate:.2f}%")
print(f"Total Profit (per share): ₹{total_profit:.2f}")

print("\nTrade-by-trade Results:")
print(results)

# --- Plot Price with Buy/Sell ---
plt.figure(figsize=(14,7))
plt.plot(data['Close'], label="Close Price", alpha=0.6)

# Buy signals
plt.scatter(data.index[(data['RSI'] < buy_level)], 
            data['Close'][data['RSI'] < buy_level], 
            label='Buy', marker='^', color='green', s=100)

# Sell signals
plt.scatter(data.index[(data['RSI'] > sell_level)], 
            data['Close'][data['RSI'] > sell_level], 
            label='Sell', marker='v', color='red', s=100)

plt.title("ADANIPOWER RSI Strategy Backtest")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()

# --- Plot RSI with thresholds ---
plt.figure(figsize=(14,5))
plt.plot(data['RSI'], label="RSI", color='purple')
plt.axhline(buy_level, color='green', linestyle='--', label='Buy Zone (40)')
plt.axhline(sell_level, color='red', linestyle='--', label='Sell Zone (60)')
plt.title("RSI Indicator with Buy/Sell Zones")
plt.xlabel("Date")
plt.ylabel("RSI Value")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()
