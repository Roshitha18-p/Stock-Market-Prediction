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
st.title("📈 NIFTY 50 Stock Prediction")

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
# LOGICAL TREND CALCULATION
# ===============================
last_30 = data.tail(30)
changes = last_30.diff().dropna()

# Use weighted trend (recent days more important)
weights = np.arange(1, len(changes)+1)
weighted_avg = np.sum(changes * weights) / np.sum(weights)

# ===============================
# NEXT DAY PREDICTION
# ===============================
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
st.title("📈 NIFTY 50 Stock Prediction")

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
# LOGICAL TREND CALCULATION
# ===============================
last_30 = data.tail(30)
changes = last_30.diff().dropna()

# Use weighted trend (recent days more important)
weights = np.arange(1, len(changes)+1)
weighted_avg = np.sum(changes * weights) / np.sum(weights)

# ===============================
# NEXT DAY PREDICTION
# ===============================
next_day_price = latest_price + weighted_avg

st.subheader("📅 Next Day Prediction")
st.success(f"{round(next_day_price,2)}")

# ===============================
# PROFIT / LOSS
# ===============================
change = next_day_price - latest_price

st.subheader("📊 Profit / Loss")

if change > 0:
    st.success(f"Profit Expected: +{round(change,2)}")
else:
    st.error(f"Loss Expected: {round(change,2)}")

# ===============================
# BUY / SELL (LOGICAL)
# ===============================
st.subheader("📢 Recommendation")

threshold = 0.002 * latest_price  # small buffer

if change > threshold:
    st.success("🟢 BUY (Upward Momentum)")
else:
    st.error("🔴 SELL (Downward Momentum)")

# ===============================
# ACCURACY (DIRECTION BASED)
# ===============================
all_changes = data.diff().dropna()

# Check how often trend direction matches
correct = 0

for i in range(1, len(all_changes)):
    if (all_changes.iloc[i] > 0 and weighted_avg > 0) or \
       (all_changes.iloc[i] < 0 and weighted_avg < 0):
        correct += 1

accuracy = (correct / len(all_changes)) * 100

st.subheader("📊 Accuracy")
st.info(f"{round(accuracy,2)}%")

# ===============================
# FOOTER
# ===============================
st.write("✅ Weighted Trend-Based Prediction Model")

st.subheader("📅 Next Day Prediction")
st.success(f"{round(next_day_price,2)}")

# ===============================
# PROFIT / LOSS
# ===============================
change = next_day_price - latest_price

st.subheader("📊 Profit / Loss")

if change > 0:
    st.success(f"Profit Expected: +{round(change,2)}")
else:
    st.error(f"Loss Expected: {round(change,2)}")

# ===============================
# BUY / SELL (LOGICAL)
# ===============================
st.subheader("📢 Recommendation")

threshold = 0.002 * latest_price  # small buffer

if change > threshold:
    st.success("🟢 BUY (Upward Momentum)")
else:
    st.error("🔴 SELL (Downward Momentum)")

# ===============================
# ACCURACY (DIRECTION BASED)
# ===============================
all_changes = data.diff().dropna()

# Check how often trend direction matches
correct = 0

for i in range(1, len(all_changes)):
    if (all_changes.iloc[i] > 0 and weighted_avg > 0) or \
       (all_changes.iloc[i] < 0 and weighted_avg < 0):
        correct += 1

accuracy = (correct / len(all_changes)) * 100

st.subheader("📊 Accuracy")
st.info(f"{round(accuracy,2)}%")

# ===============================
# FOOTER
# ===============================
st.write("✅ Weighted Trend-Based Prediction Model")
