import streamlit as st
from esg_logic import get_merchant_category, get_esg_tag, get_donation_message

st.title("🌱 ESG Tagging & Donation (Demo)")

merchant = st.text_input("Enter Merchant Name (e.g., Grab, Shopee, TNB)").strip()

if merchant:
    category = get_merchant_category(merchant)
    esg_tag = get_esg_tag(category)

    st.markdown(f"** Merchant Category:** `{category}`")
    st.markdown(f"** ESG Tag:** `{esg_tag}`")

    if esg_tag in ["High Impact", "Medium Impact"]:
        donate = st.checkbox("Donate RM0.50 to Red Cross to offset this impact")
        msg = get_donation_message(esg_tag, donate)
        if msg:
            st.success(msg)
    elif esg_tag == "Positive Impact":
        st.success("Great! This merchant supports sustainability.")
    elif esg_tag == "Low Impact":
        st.info("This merchant has minimal ESG impact.")
    elif esg_tag == "Neutral":
        st.info("stThis merchant is neutral in ESG terms.")
    else:
        st.warning("ESG info not available for this merchant.")
