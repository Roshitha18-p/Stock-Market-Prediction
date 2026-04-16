import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Stock Predictor", layout="wide")

# ===============================
# LOAD DATA & MODEL
# ===============================
df = pd.read_csv("clean_data.csv")
model = load_model("stock_model.keras")

data = df[['Close']]
dataset = data.values

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(dataset)

# ===============================
# HEADER
# ===============================
st.title("📈 NIFTY 50 Stock Prediction Dashboard")
st.markdown("AI-powered stock prediction using LSTM model")

# ===============================
# SIDEBAR INPUT
# ===============================
st.sidebar.header("🔧 Input Settings")

latest_price = st.sidebar.number_input(
    "Enter Latest Close Price",
    value=float(dataset[-1])
)

# ===============================
# NEXT DAY PREDICTION
# ===============================
last_60_days = scaled_data[-60:]
X_input = last_60_days.reshape((1, 60, 1))

pred = model.predict(X_input)
pred_price = scaler.inverse_transform(pred)[0][0]

change = pred_price - latest_price

# ===============================
# TOP METRICS
# ===============================
col1, col2, col3 = st.columns(3)

col1.metric("📅 Predicted Price", f"{round(pred_price,2)}")
col2.metric("📊 Change", f"{round(change,2)}")

if change > 0:
    col3.metric("📈 Trend", "UP")
else:
    col3.metric("📉 Trend", "DOWN")

# ===============================
# BUY / SELL / HOLD
# ===============================
st.subheader("📢 Recommendation")

threshold = 0.003 * latest_price

if change > threshold:
    st.success("🟢 BUY Signal — Price expected to rise significantly")
elif change < -threshold:
    st.error("🔴 SELL Signal — Price expected to fall")
else:
    st.warning("🟡 HOLD — Market is stable")

# ===============================
# FORECAST
# ===============================
st.subheader("📆 7-Day Forecast")

future_predictions = []
current_batch = last_60_days.copy()

for i in range(7):
    X_input = current_batch.reshape((1, 60, 1))
    pred = model.predict(X_input)

    future_predictions.append(pred[0][0])
    current_batch = np.append(current_batch[1:], pred, axis=0)

future_predictions = scaler.inverse_transform(
    np.array(future_predictions).reshape(-1,1)
)

forecast_df = pd.DataFrame({
    "Day": [f"Day {i+1}" for i in range(7)],
    "Predicted Price": [round(x[0],2) for x in future_predictions]
})

st.table(forecast_df)

# ===============================
# TREND ANALYSIS
# ===============================
st.subheader("📈 Trend Analysis")

trend = future_predictions[-1][0] - future_predictions[0][0]

if trend > 0:
    st.success("Overall Trend: UPWARD 📈")
else:
    st.error("Overall Trend: DOWNWARD 📉")

# ===============================
# CONFIDENCE
# ===============================
direction_accuracy = 52.1

st.subheader("📊 Model Confidence")
st.info(f"Direction Accuracy: {direction_accuracy}%")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("Built using Streamlit | LSTM Model | NIFTY 50 Dataset")
