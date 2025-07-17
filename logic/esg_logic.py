import json

# Load ESG tag mapping
with open("esg_tags.json", "r") as f:
    esg_tags = json.load(f)

# Load merchant to category mapping
with open("merchant_mapping.json", "r") as f:
    merchant_map = json.load(f)

def get_merchant_category(merchant_name):
    return merchant_map.get(merchant_name.strip(), "Unknown")

def get_esg_tag(category):
    return esg_tags.get(category, "Unknown")

def get_donation_message(esg_tag, donate):
    if donate:
        return "✅ Thank you! RM0.50 will be donated to the Red Cross."
    return None
