from pydantic import BaseModel


class Card(BaseModel):
        number: str
        name: str
        expDate: str
        cvv: int
        balance: float