#esg_logic.py
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

# ---- ESG Message Panel ----
def get_esg_message(tag):
    if tag == "Positive Impact":
        return "🌟 Great! This merchant supports sustainability.", "success"
    elif tag == "Low Impact":
        return "✅ This merchant has minimal ESG impact.", "info"
    elif tag == "Neutral":
        return "ℹ️ This merchant is neutral in ESG terms.", "info"
    elif tag in ["High Impact", "Medium Impact"]:
        return "⚠️ This transaction may have ESG concerns. Consider offsetting it.", "warning"
    else:
        return "⚠️ ESG info not available for this merchant.", "warning"