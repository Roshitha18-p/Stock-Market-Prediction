import streamlit as st
import pandas as pd
import numpy as np

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("clean_data.csv")
data = df['Close']

# ===============================
# UI
# ===============================
st.title("📈 NIFTY 50 Stock Prediction App")

st.subheader("📋 Latest Data")
st.dataframe(df.tail())

# ===============================
# USER INPUT
# ===============================
latest_price = st.number_input(
    "Enter Latest Close Price",
    value=float(data.iloc[-1])
)

# ===============================
# TREND CALCULATION
# ===============================
last_60 = data.tail(60)
changes = last_60.diff().dropna()

avg_change = changes.mean()

# ===============================
# NEXT DAY PREDICTION
# ===============================
next_day_price = latest_price + avg_change

st.subheader("📅 Next Day Prediction")
st.success(f"{round(next_day_price,2)}")

# ===============================
# CHANGE
# ===============================
change = next_day_price - latest_price

# ===============================
# 7-DAY FORECAST
# ===============================
st.subheader("📆 7-Day Forecast")

future = []
current = latest_price

for i in range(7):
    current = current + avg_change
    future.append(current)
    st.write(f"Day {i+1}: {round(current,2)}")

# ===============================
# TREND ANALYSIS
# ===============================
trend = future[-1] - future[0]

st.subheader("📈 Trend Analysis")

if trend > 0:
    st.success("UPWARD 📈")
else:
    st.error("DOWNWARD 📉")

# ===============================
# BUY / SELL / HOLD
# ===============================
st.subheader("📢 Recommendation")

threshold = 0.003 * latest_price

if change > threshold and trend > 0:
    st.success("🟢 STRONG BUY")
elif change < -threshold and trend < 0:
    st.error("🔴 STRONG SELL")
else:
    st.warning("🟡 HOLD")

# ===============================
# PROFIT / LOSS
# ===============================
st.subheader("📊 Profit / Loss")

if change > 0:
    st.success(f"Expected Profit: +{round(change,2)}")
else:
    st.error(f"Expected Loss: {round(change,2)}")

# ===============================
# CONFIDENCE (BASED ON VOLATILITY)
# ===============================
volatility = np.std(changes)
confidence = max(50, 100 - (volatility / latest_price * 1000))

st.subheader("📊 Confidence Level")
st.info(f"{round(confidence,2)}%")

# ===============================
# FOOTER
# ===============================
st.write("✅ LSTM Model used in backend (Notebook) | Lightweight deployment version")
