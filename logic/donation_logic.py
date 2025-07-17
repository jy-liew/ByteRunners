# donation_logic.py
import datetime
import pandas as pd

def record_donation(history_list, transaction, category, esg_tag, selected_amount):
    history_list.append({
        "Sender": transaction["sender"],
        "Merchant": transaction["recipient"],
        "Amount Donated (RM)": selected_amount,
        "Category": category,
        "ESG Tag": esg_tag,
        "Device ID": transaction["device_id"],
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
def get_donation_dataframe(history_list):
    return pd.DataFrame(history_list)
