import streamlit as st
import pandas as pd

st.title("📈 Stock Price Prediction App (NIFTY 50)")

df = pd.read_csv("clean_data.csv")
df.columns = df.columns.str.strip()

data = df['Close']

st.subheader("📊 Data Preview")
st.write(df.tail())

last_price = data.iloc[-1]

next_day = last_price * 1.002

st.subheader("📅 Next Day Prediction")
st.success(f"{next_day:.2f}")

future = []
price = last_price

for i in range(7):
    price *= 1.002
    future.append(price)

st.subheader("📊 7-Day Forecast")

for i, val in enumerate(future):
    st.write(f"Day {i+1}: {val:.2f}")

st.subheader("📉 Forecast Graph")
st.line_chart(future)
