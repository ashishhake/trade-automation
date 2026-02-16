import yfinance as yf

# Pick a stock
ticker_symbol = "INFY.NS"

# Create a Ticker object
stock = yf.Ticker(ticker_symbol)

# Get last 1 year of daily data
data = stock.history(period="6mo")

# Show first 5 rows
print(data.head())

data.to_csv("INFY.csv")
