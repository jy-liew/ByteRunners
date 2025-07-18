from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class TransactionRequest(BaseModel):
    user_id: str
    device_id: str
    amount: float
    time_of_day: str  # Format: "HH:MM"

# Response model
class RiskScoreResponse(BaseModel):
    risk_score: str
    step_up_required: bool

# Dictionary for known user-device mapping
known_devices = {
    "user_1": ["phone_1"],
    "user_2": ["desktop-2"]
}

# Main risk scoring function
def calculate_risk_score(user_id, device_id, amount, time_of_day):
    score = "LOW"
    step_up = False

    # Rule 1: High amount
    if amount >= 1000.00:
        score = "MEDIUM"

    # Rule 2: Suspicious time
    hour = int(time_of_day.split(":")[0])
    if 1 <= hour <= 5:
        score = "HIGH"

    # Rule 3: Unknown device
    if user_id in known_devices:
        if device_id not in known_devices[user_id]:
            score = "HIGH"

    if score in ["MEDIUM", "HIGH"]:
        step_up = True

    return score, step_up

transactions = []

# API route to evaluate a transaction
@app.post("/transaction", response_model=RiskScoreResponse)
def evaluate_transaction(tx: TransactionRequest):
    score, step_up = calculate_risk_score(
        tx.user_id, tx.device_id, tx.amount, tx.time_of_day
    )
    # Save transaction details
    transactions.append({
        "user": tx.user_id,
        "device": tx.device_id,
        "amount": tx.amount,
        "time": tx.time_of_day,
        "risk": score
    })
    return {
        "risk_score": score,
        "step_up_required": step_up
    }

# API route to get all transactions
@app.get("/transactions")
def get_transactions():
    return transactions
