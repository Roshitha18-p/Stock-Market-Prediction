import streamlit as st
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

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
# UI
# ===============================
st.title("📊 NIFTY 50 Stock Prediction App")

st.subheader("📋 Dataset Preview")
st.dataframe(df.tail())

# ===============================
# USER INPUT
# ===============================
st.subheader("📥 Enter Latest Closing Price")

latest_price = st.number_input(
    "Enter latest Close price",
    value=float(dataset[-1])
)

# ===============================
# NEXT DAY PREDICTION
# ===============================
last_60_days = scaled_data[-60:]
X_input = last_60_days.reshape((1, 60, 1))

pred = model.predict(X_input)
pred_price = scaler.inverse_transform(pred)[0][0]

st.subheader("📅 Next Day Prediction")
st.success(f"Predicted Price: {round(pred_price,2)}")

# ===============================
# PROFIT / LOSS
# ===============================
change = pred_price - latest_price

st.subheader("📊 Profit / Loss")

if change > 0:
    st.success(f"Profit Expected: +{round(change,2)}")
else:
    st.error(f"Loss Expected: {round(change,2)}")

# ===============================
# BUY / SELL / HOLD
# ===============================
st.subheader("📢 Recommendation")

threshold = 0.003 * latest_price  # 0.3%

if change > threshold:
    st.success("🟢 BUY Signal")
elif change < -threshold:
    st.error("🔴 SELL Signal")
else:
    st.warning("🟡 HOLD Signal")

# ===============================
# 7-DAY FORECAST
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

for i, price in enumerate(future_predictions):
    st.write(f"Day {i+1}: {round(price[0],2)}")

# ===============================
# TREND ANALYSIS
# ===============================
st.subheader("📈 Trend Analysis")

trend = future_predictions[-1][0] - future_predictions[0][0]

if trend > 0:
    st.success("Overall Trend: 📈 UPWARD")
else:
    st.error("Overall Trend: 📉 DOWNWARD")

# ===============================
# CONFIDENCE (from notebook)
# ===============================
direction_accuracy = 52.1  # update if retrained

st.subheader("📊 Model Confidence")
st.info(f"Direction Accuracy: {direction_accuracy}%")

# ===============================
# FOOTER
# ===============================
st.write("✅ Built using Streamlit | NIFTY 50 Prediction Project")
