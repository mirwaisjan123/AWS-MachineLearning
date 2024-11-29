import yfinance as yf

# Fetch historical stock data
data = yf.download("GOOG", start="2015-01-01", end="2023-01-01")

# Save the data to a CSV file
data.to_csv("google_stock_data1.csv")

print("Data saved to google_stock_data.csv")
