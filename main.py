from fastapi import FastAPI, HTTPException, status
from datetime import datetime, timedelta
from typing import List, Optional
from User import User

from Card import Card

app = FastAPI()

USERS: List[User] = [
    User(
        id=1,
        name="Andrei Popescu",
        plan="Standard",
        card=Card(number="4111222233334444", name="Andrei Popescu", expDate="12/28", cvv=123, balance=150.0),
        status="Standard",
        trial_start=None,
        trial_end=None,
        subscription_end=None,
        history=[]
    )
]


def find_user(user_id: int) -> Optional[User]:
    for user in USERS:
        if user.id == user_id:
            return user
    return None


def log_activity(user: User, action: str):
    if user.history is None:
        user.history = []
    user.history.append({
        "action": action,
        "timestamp": datetime.now().isoformat()
    })


@app.post("/subscriptions")
def subscribe(subscriber: User):
    user = find_user(subscriber.id)

    if not user:
        user = subscriber
        user.history = []
        USERS.append(user)

    now = datetime.now()
    trial_end = now + timedelta(days=7)

    user.status = "Premium (Trial)"
    user.trial_start = now.isoformat()
    user.trial_end = trial_end.isoformat()
    user.subscription_end = None

    log_activity(user, "Trial started")
    return {"message": "Subscription created in Trial mode.", "data": user}


@app.get("/subscriptions/{id}")
def check_subscription(id: int):
    user = find_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    now = datetime.now()
    response_data = user.model_dump()

    if user.status == "Premium (Trial)" and user.trial_end:
        end_time = datetime.fromisoformat(user.trial_end)
        remaining_seconds = max(0, int((end_time - now).total_seconds()))
        response_data["trial_remaining_seconds"] = remaining_seconds

    elif user.status in ["Premium (Active)", "Premium (Grace Period)"] and user.subscription_end:
        end_time = datetime.fromisoformat(user.subscription_end)
        remaining_seconds = max(0, int((end_time - now).total_seconds()))
        response_data["subscription_remaining_seconds"] = remaining_seconds

    return response_data


@app.post("/subscriptions/{id}/cancel")
def cancel_subscription(id: int):
    user = find_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.status = "Standard"
    user.trial_start = None
    user.trial_end = None
    user.subscription_end = None

    log_activity(user, "Subscription cancelled by user")
    return {"message": "Subscription cancelled.", "data": user}


@app.post("/webhooks/billing")
def handle_billing(card: Card):
    USER_ID = 1
    PRICE = 14.00
    user = find_user(USER_ID)

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    now = datetime.now()

    if card.balance >= PRICE:
        card.balance -= PRICE
        sub_end = now + timedelta(days=30)
        user.status = "Premium (Active)"
        user.trial_start = None
        user.trial_end = None
        user.subscription_end = sub_end.isoformat()
        log_activity(user, f"Payment successful")
        return {"status": "payment.succeeded"}
    else:
        grace_end = now + timedelta(days=3)
        user.status = "Premium (Grace Period)"
        user.trial_start = None
        user.trial_end = None
        user.subscription_end = grace_end.isoformat()
        log_activity(user, "Payment failed. Moved to grace period")
        return {"status": "payment.failed"}

@app.get("/subscriptions/{id}/history")
def get_subscription_history(id: int):
    user = find_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.history