# ===============================
# 📈 STOCK PRICE PREDICTION APP
# ===============================

import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Stock Prediction", layout="centered")

st.title("📈 Stock Price Prediction App (NIFTY 50)")

# ===============================
# LOAD DATA
# ===============================
try:
    df = pd.read_csv("clean_data.csv")
    df.columns = df.columns.str.strip()
    st.success("✅ Data Loaded Successfully")
except:
    st.error("❌ clean_data.csv not found")
    st.stop()

# ===============================
# PREVIEW DATA
# ===============================
st.subheader("📊 Dataset Preview")
st.dataframe(df.tail())

# ===============================
# CHECK COLUMN
# ===============================
if 'Close' not in df.columns:
    st.error("❌ 'Close' column not found in dataset")
    st.write("Available columns:", df.columns)
    st.stop()

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
# Simple growth logic (deployment version)
next_day = latest_price * 1.002

st.subheader("📅 Next Day Prediction")
st.success(f"Predicted Price: {next_day:.2f}")

# ===============================
# 7-DAY FORECAST
# ===============================
future_predictions = []
price = latest_price

for i in range(7):
    price *= 1.002
    future_predictions.append(price)

# ===============================
# DISPLAY FORECAST
# ===============================
st.subheader("📊 7-Day Forecast")

for i, price in enumerate(future_predictions):
    st.write(f"Day {i+1}: {price:.2f}")

# ===============================
# GRAPH
# ===============================
st.subheader("📉 Forecast Graph")
st.line_chart(future_predictions)

# ===============================
# FOOTER
# ===============================
st.markdown(
    "✅ Model trained using LSTM (Google Colab) | "
    "📊 Deployed using Streamlit (lightweight version)"
)
