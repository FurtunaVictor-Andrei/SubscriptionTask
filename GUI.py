import streamlit as st
import requests

USER_ID = 1
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Subscription Management", layout="centered")
st.title("📱 Client Interface - Subscription Management")

try:
    response = requests.get(f"{BASE_URL}/subscriptions/{USER_ID}")
    if response.status_code == 200:
        current_state = response.json()
    else:
        current_state = {"status": "Standard", "plan": "Standard"}
except requests.exceptions.ConnectionError:
    st.error("❌ FastAPI server is not running! Run 'uvicorn main:app --reload' first.")
    st.stop()

status_subscription = current_state.get("status", "Standard")
current_plan = current_state.get("plan", "Standard")

st.subheader("👤 Profile & Subscription Details")

col_id, col_name, col_plan = st.columns(3)
with col_id:
    st.text_input("User ID", value=str(USER_ID), disabled=True)
with col_name:
    st.text_input("Client Name", value="Andrei Popescu", disabled=True)
with col_plan:
    st.text_input("Current Plan", value=current_plan, disabled=True)

if status_subscription == "Premium (Active)":
    st.success(f"🟢 SUBSCRIPTION STATUS: {status_subscription.upper()}")
elif status_subscription in ["Premium (Trial)", "Premium (Grace Period)"]:
    st.warning(f"🟡 SUBSCRIPTION STATUS: {status_subscription.upper()}")
else:
    st.info(f"⚪ SUBSCRIPTION STATUS: {status_subscription.upper()}")

st.write("---")


@st.dialog("🛒 Confirm Premium Subscription")
def open_subscription_popup():
    st.write("### You are about to subscribe to the Premium plan!")
    st.info("ℹ️ All new subscriptions start with a **7-day free trial**.")
    st.write("After the 7-day trial expires, the subscription will cost **14.00 RON / month**.")
    st.write("---")

    user_payload = {
        "id": USER_ID,
        "name": "Andrei Popescu",
        "plan": "Premium",
        "card": {
            "number": "4111222233334444",
            "name": "Andrei Popescu",
            "expDate": "12/28",
            "cvv": 123,
            "balance": 150.0
        }
    }

    col_trial, col_direct = st.columns(2)
    with col_trial:
        if st.button("Start with 7 Days Free", use_container_width=True):
            res = requests.post(f"{BASE_URL}/subscriptions", json=user_payload)
            if res.status_code == 200:
                st.toast("Trial started successfully!", icon="🚀")
                st.rerun()

    with col_direct:
        if st.button("Pay Directly (Skip Trial)", type="primary", use_container_width=True):
            res_create = requests.post(f"{BASE_URL}/subscriptions", json=user_payload)
            if res_create.status_code == 200:
                res_webhook = requests.post(f"{BASE_URL}/webhooks/billing", json=user_payload["card"])
                if res_webhook.status_code == 200:
                    st.toast("Direct payment processed! Subscription Active.", icon="✅")
                    st.rerun()


st.subheader("⚙️ Available Actions")

disable_subscribe = status_subscription in ["Premium (Trial)", "Premium (Active)", "Premium (Grace Period)"]
disable_cancel = status_subscription not in ["Premium (Active)", "Premium (Grace Period)", "Premium (Trial)"]

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    if st.button("🚀 Subscribe to Premium", disabled=disable_subscribe, use_container_width=True):
        open_subscription_popup()
with btn_col2:
    if st.button("❌ Cancel Subscription", disabled=disable_cancel, use_container_width=True):
        res = requests.post(f"{BASE_URL}/subscriptions/{USER_ID}/cancel")
        if res.status_code == 200:
            st.toast("Subscription cancelled successfully!", icon="🛑")
            st.rerun()

st.write("---")
st.subheader("📜 System Logs")

if st.button("🔍 View Activity History", use_container_width=True):
    history_res = requests.get(f"{BASE_URL}/subscriptions/{USER_ID}/history")
    if history_res.status_code == 200:
        history_data = history_res.json()
        if history_data:
            for log in history_data:
                st.write(f"• **{log['action']}** at `{log['timestamp']}`")
        else:
            st.info("No activity found for this user.")
    else:
        st.error("Failed to fetch history from the server.")