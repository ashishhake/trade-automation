import pandas as pd
import yfinance as yf


def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Load historical market data from a CSV file.
    """

    # Read CSV file
    data = pd.read_csv(file_path)

    # Convert Date column to datetime if present
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

    # Sort by date
    data.sort_index(inplace=True)

    # Drop missing values
    data.dropna(inplace=True)

    return data


def load_yahoo_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Load real market data from Yahoo Finance and clean it for the trading bot.
    """

    # Download data from Yahoo Finance
    data = yf.download(symbol, start=start, end=end, auto_adjust=False)

    # 🔥 Fix MultiIndex columns (VERY important for yfinance)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Keep only required columns (standard OHLCV format)
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    data = data[required_cols]

    # Sort by date (oldest → newest)
    data.sort_index(inplace=True)

    # Remove NaN rows (real market data often has gaps)
    data.dropna(inplace=True)

    return data
