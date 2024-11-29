from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

# Prepare data for Prophet
data = pd.read_csv('GOOG_data.csv')  # Use your dataset
data = data.rename(columns={"Date": "ds", "Close": "y"})  # Prophet requires 'ds' for dates and 'y' for values

# Initialize and train model
model = Prophet()
model.fit(data)

# Predict future
future = model.make_future_dataframe(periods=1200)  # Predict 600 days into the future
forecast = model.predict(future)

# Plot forecast
model.plot(forecast)
plt.show()
