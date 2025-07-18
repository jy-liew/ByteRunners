#main.py
import streamlit as st
import random
from donation_logic import record_donation, get_donation_dataframe
from esg_logic import get_merchant_category, get_esg_tag, get_esg_badge, get_esg_message

st.set_page_config(page_title="ESG Demo", layout="centered")
st.markdown("""
    <div style='font-size: 36px; font-weight: 700; margin-bottom: 0.5rem;'>🌱 ESG Tagging & Red Cross Donation</div>
""", unsafe_allow_html=True)

# ---- Demo Transactions ---- 
demo_transactions = [
    {"sender": "user001", "recipient": "Grab", "amount": 25.00, "device_id": "A1"},
    {"sender": "user002", "recipient": "Shopee", "amount": 150.00, "device_id": "A2"},
    {"sender": "user003", "recipient": "TNB", "amount": 95.00, "device_id": "A3"},
    {"sender": "user004", "recipient": "Solarvest", "amount": 20.00, "device_id": "A4"},
    {"sender": "user005", "recipient": "MrDIY", "amount": 30.00, "device_id": "A5"},
    {"sender": "user006", "recipient": "AirAsia", "amount": 220.00, "device_id": "A6"},
    {"sender": "user007", "recipient": "Boost", "amount": 50.00, "device_id": "A7"},
    {"sender": "user008", "recipient": "WWF", "amount": 10.00, "device_id": "A8"}
]
## ---- Session State Initialization ----
if "total_donation" not in st.session_state:
    st.session_state.total_donation = 0.0
if "donated" not in st.session_state:
    st.session_state.donated = False
if "selected_amount" not in st.session_state:
    st.session_state.selected_amount = 0.00
if "transaction" not in st.session_state:
    st.session_state.transaction = random.choice(demo_transactions)
if "donation_history" not in st.session_state:
    st.session_state.donation_history = []

# transaction details (randomly for demo)
transaction = st.session_state.transaction
merchant_name = transaction["recipient"]
category = get_merchant_category(merchant_name)
esg_tag = get_esg_tag(category)
risk_score = random.choice(["LOW", "MEDIUM", "HIGH"])

st.session_state["risk_score"] = risk_score
risk_color = {
    "LOW": "🟢 LOW",
    "MEDIUM": "🟡 MEDIUM",
    "HIGH": "🔴 HIGH"
}
# ---- Card Layout ----
with st.container():
    st.markdown("""
    <div style='font-size: 24px; font-weight: 600; margin-top: 2rem;'>📄 Transaction Info</div>
""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**👤 Sender:** {transaction['sender']}")
        st.write(f"**🏪 Merchant:** `{merchant_name}`")
        st.write(f"**💸 Amount:** RM{transaction['amount']}")
    
    with col2:
        st.write(f"**🗂️ Category:** `{category}`")
        st.write(f"**📊 ESG Tag:** {get_esg_badge(esg_tag)}")
        st.write(f"**🆔 Device ID:** {transaction['device_id']}")
        st.markdown(f"<div style='font-size: 18px;'>🧠 <b>Risk Score:</b> {risk_color[risk_score]}</div>", unsafe_allow_html=True)


# ---- Donation ----
st.markdown("""
    <div style='font-size: 20px; font-weight: 600; margin-top: 2rem;'>❤️ Make a Donation</div>
""", unsafe_allow_html=True)

if not st.session_state.donated:
    st.session_state.selected_amount = st.selectbox(
        "Select donation amount to Red Cross",
        options=[0.00, 0.50, 1.00, 2.00, 5.00, 10.00],
        index=0,
        format_func=lambda x: f"RM{x:.2f}",
        key="donation_dropdown"
    )
    if st.button("✅ Donate Now"):
        if st.session_state.selected_amount > 0:
            st.session_state.total_donation += st.session_state.selected_amount
            record_donation(
                st.session_state.donation_history,
                transaction,
                category,
                esg_tag,
                st.session_state.selected_amount
            )
            st.session_state.donated = True
            st.rerun()
        else:
            st.info("ℹ️ Please select a donation amount greater than RM0.00.")
else:
    st.selectbox(
        "Select donation amount to Red Cross",
        options=[st.session_state.selected_amount],
        index=0,
        disabled=True,
        format_func=lambda x: f"RM{x:.2f}",
        key="donation_dropdown"
    )
    st.button("✅ Donate Now", disabled=True)
    st.success(f"🎉 Thank you! RM{st.session_state.selected_amount:.2f} has been donated to the Red Cross.")

# ---- ESG Message Panel ----
msg, msg_type = get_esg_message(esg_tag)
getattr(st, msg_type)(msg)

# ---- total donation Summary ----
st.markdown("""
    <div style='font-size: 20px; font-weight: 600; margin-top: 2rem;'>💰 Total Donations Contributed</div>
""", unsafe_allow_html=True)
st.markdown(f"<div style='font-size: 18px;'>RM {st.session_state.total_donation:.2f}</div>", unsafe_allow_html=True)

#---- donation history ---- view all past 7 donations, download for full donation history
st.markdown("""<div style='font-size: 20px; font-weight: 600;'>📖 Donation History</div>""", unsafe_allow_html=True)

with st.expander("💾 View All Past Donations", expanded=False):
    if st.session_state.donation_history:
        df = get_donation_dataframe(st.session_state.donation_history)
        st.dataframe(df.tail(10), use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Full History as CSV",
            data=csv,
            file_name="donation_history.csv",
            mime="text/csv"
        )
    else:
        st.info("No donations recorded yet.")

# ---- Refresh Button ---- (for demo purposes)
if st.button("🔁 Generate New Transaction (Demo)"):
    st.session_state.transaction = random.choice(demo_transactions)
    st.session_state.donated = False
    st.session_state.selected_amount = 0.00
    st.rerun()

