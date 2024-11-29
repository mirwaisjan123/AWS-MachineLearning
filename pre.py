import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Load the dataset
data = pd.read_csv("GOOG_data.csv")  # Replace with your actual CSV file
data = data['Close'].values.reshape(-1, 1)  # Use the 'Close' column for predictions

# Scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Prepare training data
look_back = 600  # Use the last 30 days to predict the future
x_train, y_train = [], []

for i in range(look_back, len(scaled_data)):
    x_train.append(scaled_data[i - look_back:i, 0])
    y_train.append(scaled_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Build the LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)),
    LSTM(50, return_sequences=False),
    Dense(25),
    Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(x_train, y_train, batch_size=32, epochs=20)

# Predict the next 30 days
last_30_days = scaled_data[-look_back:]  # Get the last 30 days of data
predictions = []

for _ in range(900):  # Predict for 30 days
    last_30_days_reshaped = np.reshape(last_30_days, (1, look_back, 1))
    next_day = model.predict(last_30_days_reshaped, verbose=0)
    predictions.append(next_day[0, 0])
    last_30_days = np.append(last_30_days[1:], next_day, axis=0)

# Rescale predictions back to original scale
predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(data, label="Historical Prices", color="blue")
plt.plot(range(len(data), len(data) + 900), predicted_prices, label="Predicted Prices (Next 900 Days)", color="red")
plt.title("Stock Price Prediction")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()
