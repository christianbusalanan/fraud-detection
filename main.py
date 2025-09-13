import streamlit as st

st.set_page_config(layout="wide")
pages = {
    "Fraud Detection": [
        st.Page("app/pages/dashboard.py", title="Dashboard", icon="🖥️"),
        st.Page("app/pages/transactions.py", title="Transactions", icon="🏛️"),
        st.Page("app/pages/model.py", title="Model", icon="⚙️"),
    ]
}

pg = st.navigation(pages, position="top")
pg.run()