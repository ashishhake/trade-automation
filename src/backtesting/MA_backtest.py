import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download Data
data = yf.download("^NSEBANK", start="2024-01-01", end="2025-08-14", interval="1h", auto_adjust=True)

# Calculate Moving Averages
data['MA9'] = data['Close'].rolling(window=9).mean()
data['MA21'] = data['Close'].rolling(window=21).mean()

# Vectorized signal logic
data['Signal'] = 0
data['Signal'] = (data['MA9'] > data['MA21']).astype(int)
data['Position'] = data['Signal'].diff()  # 1 = buy, -1 = sell

# ----------------- BACKTESTING PART -----------------
trades = []
buy_price = None

for i in range(len(data)):
    if data['Position'].iloc[i] == 1:   # Buy signal
        buy_price = float(data['Close'].iloc[i])

    elif data['Position'].iloc[i] == -1 and buy_price is not None:  # Sell signal
        sell_price = float(data['Close'].iloc[i])

        profit = sell_price - buy_price
        trades.append(profit)

        buy_price = None  # reset



# ✅ Remove NaN issues by directly creating DataFrame from trades list
results = pd.DataFrame({'Profit_per_Trade': trades})

# 🔑 Ensure values are numeric
results = pd.DataFrame({'Profit_per_Trade': trades})
results['Cumulative_Profit'] = results['Profit_per_Trade'].cumsum()

total_trades = len(results)
winning_trades = (results['Profit_per_Trade'] > 0).sum()
losing_trades = (results['Profit_per_Trade'] <= 0).sum()
win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
total_profit = results['Profit_per_Trade'].sum()


print("📊 Backtest Results")
print(f"Total Trades: {total_trades}")
print(f"Winning Trades: {winning_trades}")
print(f"Losing Trades: {losing_trades}")
print(f"Win Rate: {win_rate:.2f}%")
print(f"Total Profit (per share): ₹{total_profit:.2f}")

# ----------------- PLOT -----------------
plt.figure(figsize=(14,7))
plt.plot(data['Close'], label="Close Price", alpha=0.5)
plt.plot(data['MA9'], label="MA 9", color='blue')
plt.plot(data['MA21'], label="MA 21", color='orange')

# Buy signals
plt.scatter(data.index[data['Position'] == 1], 
            data['Close'][data['Position'] == 1], 
            label='Buy', marker='^', color='green', s=100)

# Sell signals
plt.scatter(data.index[data['Position'] == -1], 
            data['Close'][data['Position'] == -1], 
            label='Sell', marker='v', color='red', s=100)

plt.title("^NSEBANK Moving Average Buy/Sell Strategy with Backtest")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.legend(loc="upper left")
plt.grid(True)
plt.show()

# Show trade results
print("\nTrade-by-trade Results:")
print(results)
