from pydantic import BaseModel, Field
from datetime import date

from enum import Enum

class ExpenseType(str, Enum):
    income = "income"
    expense = "expense"

class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: ExpenseType
    category: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    expense_date: date