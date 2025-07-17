import streamlit as st
import random
import pandas as pd
import datetime
from esg_logic import get_merchant_category, get_esg_tag, get_donation_message

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


# 🔄 Randomly choose one transaction
transaction = st.session_state.transaction
merchant_name = transaction["recipient"]
category = get_merchant_category(merchant_name)
esg_tag = get_esg_tag(category)

# ---- ESG Badge Display ----
def get_esg_badge(tag):
    badge_map = {
        "High Impact": "🟥 High Impact",
        "Medium Impact": "🟧 Medium Impact",
        "Low Impact": "🟩 Low Impact",
        "Positive Impact": "🟦 Positive Impact",
        "Neutral": "⬜ Neutral",
        "Unknown": "⬛ Unknown"
    }
    return badge_map.get(tag, "⬛ Unknown")

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
            
            # Save donation entry to history
            st.session_state.donation_history.append({
                "Sender": transaction["sender"],
                "Merchant": merchant_name,
                "Amount Donated (RM)": st.session_state.selected_amount,
                "Category": category,
                "ESG Tag": esg_tag,
                "Device ID": transaction["device_id"],
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
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
if esg_tag == "Positive Impact":
    st.success("🌟 Great! This merchant supports sustainability.")
elif esg_tag == "Low Impact":
    st.info("✅ This merchant has minimal ESG impact.")
elif esg_tag == "Neutral":
    st.info("ℹ️ This merchant is neutral in ESG terms.")
elif esg_tag in ["High Impact", "Medium Impact"]:
    st.warning("⚠️ This transaction may have ESG concerns. Consider offsetting it.")
else:
    st.warning("⚠️ ESG info not available for this merchant.")

# ---- Donation Summary ----
st.markdown("""
    <div style='font-size: 20px; font-weight: 600; margin-top: 2rem;'>💰 Total Donations Contributed</div>
""", unsafe_allow_html=True)
st.markdown(f"<div style='font-size: 18px;'>RM {st.session_state.total_donation:.2f}</div>", unsafe_allow_html=True)

#---- donation history ----
st.markdown("""<div style='font-size: 20px; font-weight: 600;'>📖 Donation History</div>""", unsafe_allow_html=True)

with st.expander("💾 View All Past Donations", expanded=False):
    if st.session_state.donation_history:
        df = pd.DataFrame(st.session_state.donation_history)
        st.dataframe(df.tail(10), use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Full History as CSV",
            data=csv,
            file_name="donation_history.csv",
            mime="text/csv"
        )
    else:
        st.info("No donations recorded yet.")



# ---- Refresh Button ----
if st.button("🔁 Generate New Transaction"):
    st.session_state.transaction = random.choice(demo_transactions)
    st.session_state.donated = False
    st.session_state.selected_amount = 0.00
    st.rerun()

