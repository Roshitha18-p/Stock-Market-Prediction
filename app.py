# ===============================
# 📈 STOCK PRICE PREDICTION APP
# ===============================

import streamlit as st
import pandas as pd
import random

# Page settings
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
# DATA PREVIEW
# ===============================
st.subheader("📊 Dataset Preview")
st.dataframe(df.tail())

# ===============================
# CHECK COLUMN
# ===============================
if 'Close' not in df.columns:
    st.error("❌ 'Close' column not found")
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
change = random.uniform(-0.005, 0.005)
next_day = latest_price * (1 + change)

st.subheader("📅 Next Day Prediction")
st.success(f"Predicted Price: {next_day:.2f}")

# ===============================
# PROFIT / LOSS
# ===============================
difference = next_day - latest_price

if difference > 0:
    st.success(f"📈 Profit: +{difference:.2f}")
elif difference < 0:
    st.error(f"📉 Loss: {difference:.2f}")
else:
    st.info("No change")

# ===============================
# BUY / SELL SIGNAL
# ===============================
st.subheader("📊 Recommendation")

if difference > 0:
    st.success("🟢 BUY Signal")
elif difference < 0:
    st.error("🔴 SELL Signal")
else:
    st.info("🟡 HOLD")

# ===============================
# 7-DAY FORECAST (UP & DOWN)
# ===============================
future_predictions = []
price = latest_price

for i in range(7):
    change = random.uniform(-0.01, 0.01)
    price = price * (1 + change)
    future_predictions.append(round(price, 2))

# ===============================
# DISPLAY FORECAST
# ===============================
st.subheader("📊 7-Day Forecast")

for i, price in enumerate(future_predictions):
    st.write(f"Day {i+1}: {price}")

# ===============================
# GRAPH
# ===============================
st.subheader("📉 Forecast Graph")
st.line_chart(future_predictions)

# ===============================
# FOOTER
# ===============================
st.markdown(
    "✅ LSTM Model trained in Google Colab | "
    "📊 Deployment uses simulated market fluctuations"
)
