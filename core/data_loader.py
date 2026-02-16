import pandas as pd


def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Load historical market data from a CSV file.

    Parameters:
    file_path (str): Path to the CSV file containing market data

    Returns:
    pd.DataFrame: Cleaned pandas DataFrame with market data
    """

    # Read CSV file into pandas DataFrame
    data = pd.read_csv(file_path)

    # Convert 'Date' column to datetime (VERY important in trading)
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])

    # Set Date as index (standard practice in trading systems)
    if 'Date' in data.columns:
        data.set_index('Date', inplace=True)

    # Sort data by date (oldest → newest)
    data.sort_index(inplace=True)

    return data
