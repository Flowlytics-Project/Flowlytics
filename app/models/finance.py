from sqlmodel import SQLModel, Field, Relationship 
from typing import Optional, TYPE_CHECKING 
from datetime import datetime, date, timezone 
from enum import Enum 

if TYPE_CHECKING: 
    from app.models.user import User 

class TransactionCategory(str, Enum): 
    FOOD = "food"
    TRANSPORT = "transport"
    HOUSING = "housing"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health" 
    EDUCATION = "education"
    CLOTHING = "clothing"
    UTILITIES = "utilities"
    OTHER = "other" 

class BillingCycle(str, Enum): 
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class BudgetPeriod(str, Enum): 
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class Transaction(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True) 
    user_id: int = Field(foreign_key="user.id", index=True) 
    amount: float
    category: TransactionCategory = TransactionCategory.OTHER
    description: str = "" 
    transaction_date: date = Field(default_factory=lambda: date.today()) 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  

    user: Optional["User"] = Relationship(back_populates="transactions") 

class Subscription(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True) 
    user_id: int = Field(foreign_key="user.id", index=True) 
    name: str
    amount: float
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    next_due: date 
    active: bool = True 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 

    user: Optional["User"] = Relationship(back_populates="subscriptions") 

class Budget(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True) 
    user_id: int = Field(foreign_key="user.id", index=True) 
    category: TransactionCategory
    limit_amount: float
    period: BudgetPeriod = BudgetPeriod.MONTHLY
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 

    user: Optional["User"] = Relationship(back_populates="budgets")

class Income(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True) 
    user_id: int = Field(foreign_key="user.id", index=True) 
    source: str 
    amount: float
    income_date: date = Field(default_factory=lambda: date.today()) 
    is_recurring: bool = False
    recurrence_period: Optional[BudgetPeriod] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 

    user: Optional["User"] = Relationship(back_populates="incomes")