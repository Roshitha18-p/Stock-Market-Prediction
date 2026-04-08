import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("📈 Stock Price Prediction App (NIFTY 50)")

# Load data
df = pd.read_csv("clean_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Use Close column (your dataset confirmed)
data = df['Close']

# Show data
st.subheader("📊 Data Preview")
st.write(df.tail())

# Last price
last_price = data.iloc[-1]

# Next day prediction
next_day = last_price * 1.002

st.subheader("📅 Next Day Prediction")
st.success(f"Predicted Price: {next_day:.2f}")

# 7-day forecast
future = []
price = last_price

for i in range(7):
    price *= 1.002
    future.append(price)

st.subheader("📊 7-Day Forecast")

for i, val in enumerate(future):
    st.write(f"Day {i+1}: {val:.2f}")

# Graph
st.subheader("📉 Forecast Graph")

plt.figure()
plt.plot(future, marker='o')
plt.title("7-Day Forecast")
plt.xlabel("Days")
plt.ylabel("Price")

st.pyplot(plt)