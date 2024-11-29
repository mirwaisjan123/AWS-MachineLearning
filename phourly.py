import yfinance as yf
import json

# List of stock tickers
tickers = ["GOOG", "AAPL", "MSFT", "AMZN", "TSLA"]

# Date range for hourly data (must be within the last ~2 years as per Yahoo Finance limits)
start_date = "2023-01-01"
end_date = "2023-11-25"

# Dictionary to store data for all tickers
all_data = {}

# Fetch hourly data for each ticker
for ticker in tickers:
    print(f"Fetching hourly data for {ticker}...")
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval="1h")

        # Check if data is empty
        if data.empty:
            print(f"No hourly data available for {ticker}. Skipping.")
            continue

        # Reset index to make Datetime a column
        data = data.reset_index()

        # Ensure all keys are strings and JSON-compatible
        data['Datetime'] = data['Datetime'].astype(str)  # Convert Datetime column to string
        data.columns = [str(col) for col in data.columns]  # Ensure column names are strings

        # Convert the DataFrame to a JSON-serializable dictionary
        data_dict = data.to_dict(orient="records")
        all_data[ticker] = data_dict
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")

# Save all data to a JSON file
output_file = "hourly_stock_data.json"
try:
    with open(output_file, "w") as json_file:
        json.dump(all_data, json_file, indent=4)
    print(f"Hourly data for {', '.join(tickers)} has been saved to {output_file}.")
except Exception as e:
    print(f"Failed to save data to {output_file}: {e}")
