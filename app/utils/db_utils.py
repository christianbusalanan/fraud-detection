import pandas as pd
import streamlit as st

# Initialize Streamlit connection
conn = st.connection("postgres", type="sql")

# -------------------------------
# Utility Functions
# -------------------------------

def fetch_dataframe(query: str, params: dict = None) -> pd.DataFrame:
    """
    Run a SELECT query and return results as a pandas DataFrame.
    Example:
        df = fetch_dataframe("SELECT * FROM transactions LIMIT 10;")
    """
    # Reset index to start at 1 instead of 0
    df = conn.query(query, params=params)

    # Reset index to start at 1 instead of 0
    df.index = range(1, len(df) + 1)
    return df


def execute_query(query: str, params: dict = None) -> None:
    """
    Run an INSERT, UPDATE, or DELETE query.
    """
    with conn.session as session:
        session.execute(query, params or {})
        session.commit()


def insert_transaction(origin: int, dest: int, amount: float, fraud: bool = False) -> None:
    """
    Insert a new transaction.
    """
    query = """
        INSERT INTO transactions (account_origin, account_destination, amount, is_fraud)
        VALUES (:origin, :dest, :amount, :fraud)
    """
    execute_query(query, {"origin": origin, "dest": dest, "amount": amount, "fraud": fraud})


def insert_model_log(transaction_id: int, predicted_label: bool, prediction_score: float, explanation: dict) -> None:
    """
    Insert model prediction log with explanation (JSON).
    """
    query = """
        INSERT INTO model_logs (transaction_id, predicted_label, prediction_score, explanation_json)
        VALUES (:tid, :label, :score, :explanation)
    """
    execute_query(query, {
        "tid": transaction_id,
        "label": predicted_label,
        "score": prediction_score,
        "explanation": explanation
    })


def get_pending_alerts(limit: int = 10) -> pd.DataFrame:
    """
    Fetch pending fraud alerts for review.
    """
    query = """
        SELECT a.alert_id, t.transaction_id, t.amount, a.detected_at, a.status
        FROM fraud_alerts a
        JOIN transactions t ON a.transaction_id = t.transaction_id
        WHERE a.status = 'pending'
        ORDER BY a.detected_at DESC
        LIMIT :limit
    """
    return fetch_dataframe(query, {"limit": limit})
