# ===============================
# 📊 STOCK MARKET PREDICTION APP
# ===============================

import streamlit as st
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# ===============================
# 1. PAGE CONFIG
# ===============================
st.set_page_config(page_title="Stock Prediction AI", layout="centered")

st.title("📈 Stock Market Prediction AI")
st.write("Next day prediction + Buy/Sell/Hold signal + Forecast")

# ===============================
# 2. LOAD DATA & MODEL
# ===============================
@st.cache_resource
def load_assets():
    df = pd.read_csv("clean_data.csv")
    model = load_model("stock_model.keras")
    return df, model

df, model = load_assets()

st.success("Model & Data Loaded Successfully")

# ===============================
# 3. PREPROCESS DATA
# ===============================
data = df[['Close']]
dataset = data.values

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

training_data_len = int(len(scaled_data) * 0.8)

test_data = scaled_data[training_data_len - 60:]

X_test = []
y_test = dataset[training_data_len:]

for i in range(60, len(test_data)):
    X_test.append(test_data[i-60:i, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# ===============================
# 4. PREDICTIONS
# ===============================
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

y_test = y_test.reshape(-1, 1)

# ===============================
# 5. METRICS
# ===============================
rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
mae = np.mean(np.abs(predictions - y_test))

accuracy = 100 - (np.mean(np.abs((y_test - predictions) / y_test)) * 100)

direction_correct = np.sum(
    np.sign(y_test[1:] - y_test[:-1]) ==
    np.sign(predictions[1:] - predictions[:-1])
)
direction_accuracy = (direction_correct / len(y_test)) * 100

# ===============================
# 6. NEXT DAY PREDICTION
# ===============================
last_60_days = scaled_data[-60:]
X_input = last_60_days.reshape(1, 60, 1)

next_day_scaled = model.predict(X_input)
next_day_price = scaler.inverse_transform(next_day_scaled)[0][0]

latest_price = dataset[-1][0]
change = next_day_price - latest_price

# ===============================
# 7. BUY / SELL / HOLD
# ===============================
threshold = 0.003 * latest_price

if change > threshold:
    signal = "🟢 BUY"
elif change < -threshold:
    signal = "🔴 SELL"
else:
    signal = "🟡 HOLD"

# ===============================
# 8. UI OUTPUT
# ===============================
st.subheader("📊 Model Performance")

st.write("RMSE:", round(rmse, 2))
st.write("MAE:", round(mae, 2))
st.write("Accuracy:", round(accuracy, 2), "%")
st.write("Direction Accuracy:", round(direction_accuracy, 2), "%")

st.subheader("📅 Next Day Prediction")
st.write("Predicted Price:", round(next_day_price, 2))
st.write("Change:", round(change, 2))

st.subheader("📢 Recommendation")
st.success(signal)

# ===============================
# 9. 7 DAY FORECAST
# ===============================
future_predictions = []
current_batch = last_60_days.copy()

for i in range(7):
    X_input = current_batch.reshape(1, 60, 1)
    pred = model.predict(X_input)

    future_predictions.append(pred[0][0])
    current_batch = np.append(current_batch[1:], pred, axis=0)

future_predictions = scaler.inverse_transform(
    np.array(future_predictions).reshape(-1, 1)
)

st.subheader("📆 7-Day Forecast")

for i, price in enumerate(future_predictions):
    st.write(f"Day {i+1}: {round(price[0], 2)}")

# ===============================
# 10. TREND
# ===============================
trend = future_predictions[-1][0] - future_predictions[0][0]

st.subheader("📈 Trend Analysis")

if trend > 0:
    st.success("Overall Trend: UPWARD 📈")
else:
    st.error("Overall Trend: DOWNWARD 📉")

# ===============================
# 11. CONFIDENCE
# ===============================
st.subheader("📊 Confidence Level")
st.write(round(direction_accuracy, 2), "%")
