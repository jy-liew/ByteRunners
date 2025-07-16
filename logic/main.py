import streamlit as st
from esg_logic import get_merchant_category, get_esg_tag, get_donation_message

st.title("🌱 ESG Tagging & Donation (Demo)")

# demo transaction data 
transaction = {
    "sender": "user123",
    "recipient": "Grab",   
    "amount": 42.50,
    "time": "2025-07-16 21:45",
    "device_id": "abc123"
}

# extract merchant from transaction
merchant_name = transaction["recipient"]

# ESG tagging logic
category = get_merchant_category(merchant_name)
esg_tag = get_esg_tag(category)

# output
st.markdown(f"**🧾 Merchant:** `{merchant_name}`")
st.markdown(f"**🗂️ Category:** `{category}`")
st.markdown(f"**📊 ESG Tag:** `{esg_tag}`")

# donation
donate = st.checkbox("Donate RM0.50 to Red Cross to support global humanitarian aid")
msg = get_donation_message(esg_tag, donate)
if msg:
    st.success(msg)

# ESG feedback message
if esg_tag == "Positive Impact":
    st.success("🌟 Great! This merchant supports sustainability.")
elif esg_tag == "Low Impact":
    st.info("✅ This merchant has minimal ESG impact.")
elif esg_tag == "Neutral":
    st.info("ℹ️ This merchant is neutral in ESG terms.")
elif esg_tag in ["High Impact", "Medium Impact"]:
    st.warning("⚠️ This transaction has ESG concerns. Consider offsetting it.")
else:
    st.warning("⚠️ ESG info not available for this merchant.")
