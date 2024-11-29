import yfinance as yf
import json

# List of stock tickers
tickers = ["GOOG", "AAPL", "MSFT", "AMZN", "TSLA"]

# Date range
start_date = "2013-01-01"
end_date = "2024-10-01"

# Dictionary to store data for all tickers
all_data = {}

# Fetch data for each ticker
for ticker in tickers:
    print(f"Fetching data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)

    # Reset index to make Date a column
    data = data.reset_index()

    # Rename columns to remove tuple-like names
    data = data.rename(columns={
        "Date": "Date",
        "Adj Close": "Adj Close",
        "Close": "Close",
        "High": "High",
        "Low": "Low",
        "Open": "Open",
        "Volume": "Volume"
    })

    # Ensure all keys are JSON-compatible
    data["Date"] = data["Date"].astype(str)  # Convert Date column to string
    data_dict = data.to_dict(orient="records")
    all_data[ticker] = data_dict

# Save all data to a JSON file
output_file = "stock_data.json"
with open(output_file, "w") as json_file:
    json.dump(all_data, json_file, indent=4)

print(f"Data for {', '.join(tickers)} has been saved to {output_file}.")
