from pydantic import BaseModel
from typing import List, Optional
from Card import Card

class User(BaseModel):
    id: int
    name: str
    card: Card
    plan: str
    status: Optional[str] = "Standard"
    trial_start: Optional[str] = None
    trial_end: Optional[str] = None
    subscription_end: Optional[str] = None
    history: Optional[List[dict]] = []