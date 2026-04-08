import streamlit as st
import pandas as pd

# ===============================
# TITLE
# ===============================
st.title("📈 Stock Price Prediction App (NIFTY 50)")

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("clean_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Use Close column
data = df['Close']

# ===============================
# SHOW DATA
# ===============================
st.subheader("📊 Dataset Preview")
st.write(df.tail())

# ===============================
# USER INPUT
# ===============================
st.subheader("🧾 Enter Latest Closing Price")

default_price = float(data.iloc[-1])

user_input = st.number_input(
    "Enter latest Close price",
    value=default_price,
    step=1.0
)

# ===============================
# NEXT DAY PREDICTION
# ===============================
next_day = user_input * 1.002

st.subheader("📅 Next Day Prediction")
st.success(f"Predicted Price: {next_day:.2f}")

# ===============================
# 7-DAY FORECAST
# ===============================
future = []
price = user_input

for i in range(7):
    price *= 1.002
    future.append(price)

st.subheader("📊 7-Day Forecast")

for i, val in enumerate(future):
    st.write(f"Day {i+1}: {val:.2f}")

# ===============================
# GRAPH (NO MATPLOTLIB)
# ===============================
st.subheader("📉 Forecast Graph")
st.line_chart(future)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("✅ Built using Streamlit | 📊 NIFTY 50 Prediction Project")
