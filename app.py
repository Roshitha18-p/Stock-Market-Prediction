# ===============================
# 📈 STOCK PRICE PREDICTION APP
# ===============================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Stock Prediction", layout="wide")

st.title("📈 Stock Price Prediction App (NIFTY 50)")

# ===============================
# LOAD DATA
# ===============================
try:
    df = pd.read_csv("clean_data.csv")
    st.success("✅ Data Loaded Successfully")
except:
    st.error("❌ clean_data.csv not found")
    st.stop()

# ===============================
# CHECK COLUMN
# ===============================
if 'Close' not in df.columns:
    st.error("❌ 'Close' column not found in dataset")
    st.write("Available columns:", df.columns)
    st.stop()

# ===============================
# PREVIEW DATA
# ===============================
st.subheader("📊 Dataset Preview")
st.dataframe(df.tail())

# ===============================
# LOAD MODEL
# ===============================
try:
    model = load_model("stock_model.keras")
    st.success("✅ Model Loaded Successfully")
except:
    st.error("❌ Model not found")
    st.stop()

# ===============================
# PREPARE DATA
# ===============================
data = df[['Close']]
dataset = data.values

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# ===============================
# USER INPUT
# ===============================
st.subheader("🧾 Enter Latest Closing Price")

latest_price = st.number_input(
    "Enter latest Close price",
    value=float(df['Close'].iloc[-1])
)

# ===============================
# NEXT DAY PREDICTION
# ===============================
last_60_days = scaled_data[-60:]
X_input = np.array([last_60_days])
X_input = X_input.reshape((1, 60, 1))

next_day = model.predict(X_input)
next_day_price = scaler.inverse_transform(next_day)

st.subheader("📅 Next Day Prediction")
st.success(f"Predicted Price: {next_day_price[0][0]:.2f}")

# ===============================
# 7-DAY FORECAST (CORRECT LOGIC)
# ===============================
future_predictions = []
current_batch = last_60_days.copy()

for i in range(7):
    current_batch_reshaped = current_batch.reshape((1, 60, 1))
    
    pred = model.predict(current_batch_reshaped)
    
    future_predictions.append(pred[0][0])
    
    current_batch = np.append(current_batch[1:], pred, axis=0)

future_predictions = scaler.inverse_transform(
    np.array(future_predictions).reshape(-1, 1)
)

# ===============================
# DISPLAY FORECAST
# ===============================
st.subheader("📊 7-Day Forecast")

for i, price in enumerate(future_predictions):
    st.write(f"Day {i+1}: {price[0]:.2f}")

# ===============================
# GRAPH
# ===============================
st.subheader("📉 Forecast Graph")

plt.figure(figsize=(8, 4))
plt.plot(range(1, 8), future_predictions, marker='o')
plt.title("7-Day Prediction")
plt.xlabel("Days")
plt.ylabel("Price")
plt.grid()

st.pyplot(plt)

# ===============================
# FOOTER
# ===============================
st.markdown("✅ Built using Streamlit | 📊 NIFTY 50 Prediction Project")
