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
std_dev = changes.std()

# ===============================
# NEXT DAY PREDICTION (DYNAMIC)
# ===============================
random_change = np.random.normal(avg_change, std_dev)
next_day_price = latest_price + random_change

st.subheader("📅 Next Day Prediction")
st.success(f"{round(next_day_price,2)}")

# ===============================
# CHANGE
# ===============================
change = next_day_price - latest_price

# ===============================
# 7-DAY FORECAST (DYNAMIC)
# ===============================
st.subheader("📆 7-Day Forecast")

future = []
current = latest_price

for i in range(7):
    random_change = np.random.normal(avg_change, std_dev)
    current = current + random_change
    future.append(current)
    st.write(f"Day {i+1}: {round(current,2)}")

# ===============================
# TREND ANALYSIS
# ===============================
trend = future[-1] - future[0]

st.subheader("📈 Trend Analysis")

if trend > 0:
    st.success("Overall Trend: UPWARD 📈")
else:
    st.error("Overall Trend: DOWNWARD 📉")

# ===============================
# BUY / SELL / HOLD
# ===============================
st.subheader("📢 Recommendation")

threshold = 0.003 * latest_price  # 0.3%

if change > threshold and trend > 0:
    st.success("🟢 STRONG BUY Signal")
elif change < -threshold and trend < 0:
    st.error("🔴 STRONG SELL Signal")
else:
    st.warning("🟡 HOLD Signal")

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

# Confidence formula (stable = higher confidence)
confidence = max(50, 100 - (volatility / latest_price * 1000))

st.subheader("📊 Confidence Level")
st.info(f"{round(confidence,2)}%")

# ===============================
# FOOTER
# ===============================
st.write("✅ Trend + Volatility Based Prediction (Lightweight Deployment Version)")
