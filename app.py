from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Input

app = Flask(__name__)

DATA_PATH = "data/"
LOOK_BACK = 30  # Number of days to look back for predictions


def load_and_scale_data(file_path):
    # Load and scale data
    data = pd.read_csv(file_path)['Close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    return data, scaled_data, scaler


def create_lstm_model(input_shape):
    # Build LSTM model
    model = Sequential([
        Input(shape=input_shape),  # Explicit Input layer
        LSTM(50, return_sequences=True),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        company = data.get('company')  # Extract selected company
        days_to_predict = int(data.get('days'))  # Extract prediction duration

        if not company or days_to_predict <= 0:
            return jsonify({"error": "Invalid input. 'company' and 'days' are required."}), 400

        file_path = os.path.join(DATA_PATH, f"{company}_data.csv")
        if not os.path.exists(file_path):
            return jsonify({"error": "Data for the selected company does not exist."}), 400

        # Load and prepare data
        historical_data, scaled_data, scaler = load_and_scale_data(file_path)

        # Prepare training data
        x_train, y_train = [], []
        for i in range(LOOK_BACK, len(scaled_data)):
            x_train.append(scaled_data[i - LOOK_BACK:i, 0])
            y_train.append(scaled_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Train the model
        model = create_lstm_model((x_train.shape[1], 1))
        model.fit(x_train, y_train, batch_size=32, epochs=10, verbose=0)

        # Predict future prices
        last_days = scaled_data[-LOOK_BACK:]
        predictions = []
        for _ in range(days_to_predict):
            last_days_reshaped = np.reshape(last_days, (1, LOOK_BACK, 1))
            next_day = model.predict(last_days_reshaped, verbose=0)
            predictions.append(next_day[0, 0])
            last_days = np.append(last_days[1:], next_day, axis=0)

        # Rescale predictions to original scale
        predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

        return jsonify({
            "predictions": predicted_prices.tolist(),
            "historical_data": historical_data.flatten().tolist()  # Send historical data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
