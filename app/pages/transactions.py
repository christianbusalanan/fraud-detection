import streamlit as st
import pandas as pd
from app.utils import db_utils as db

st.logo("assets/logo.png", icon_image="assets/logo.png")
st.markdown("## Transactions")

df = db.fetch_dataframe("SELECT * FROM transaction order by transaction_time desc")

# Create two columns for filters
col1, col2 = st.columns(2)

with col1:
    selected_type = st.selectbox(
        "Filter by Transaction Type:",
        options=["All"] + list(df["transaction_type"].unique())
    )

with col2:
    selected_fraud = st.selectbox(
        "Filter by Fraud Label:",
        options=["All", "Fraudulent", "Not Fraudulent"]
    )

# Apply transaction type filter
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df["transaction_type"] == selected_type]

# Apply fraud filter
if selected_fraud == "Fraudulent":
    filtered_df = filtered_df[filtered_df["is_fraud"] == 1]
elif selected_fraud == "Not Fraudulent":
    filtered_df = filtered_df[filtered_df["is_fraud"] == 0]

st.dataframe(filtered_df, height=400)