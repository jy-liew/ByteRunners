import streamlit as st
from esg_logic import get_merchant_category, get_esg_tag, get_donation_message
from esg_logic import merchant_map 

st.title("🌱  ESG Tagging & Donation")


merchant = st.selectbox("Select a Merchant", list(merchant_map.keys()))


if merchant:
    category = get_merchant_category(merchant)
    esg_tag = get_esg_tag(category)

    st.markdown(f"**🧾 Merchant Category:** `{category}`")
    st.markdown(f"**📊 ESG Tag:** `{esg_tag}`")

    if esg_tag in ["High Impact", "Medium Impact"]:
        donate = st.checkbox("Donate RM0.50 to Red Cross to offset this impact")
        msg = get_donation_message(esg_tag, donate)
        if msg:
            st.success(msg)
    elif esg_tag == "Positive Impact":
        st.success("🌟 Great! This merchant supports sustainability.")
    elif esg_tag == "✅ Low Impact":
        st.info("ℹ️ This merchant has minimal ESG impact.")
    elif esg_tag == "Neutral":
        st.info("stThis merchant is neutral in ESG terms.")
    else:
        st.warning("⚠️ ESG info not available for this merchant.")
