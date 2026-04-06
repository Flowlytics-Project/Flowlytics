from sqlmodel import SQLModel
from typing import Optional
from datetime import date, datetime 
from app.models.finance import TransactionCategory, BillingCycle, BudgetPeriod 

# -- Transaction -- 

class TransactionCreate(SQLModel):
    amount: float
    category: TransactionCategory = TransactionCategory.OTHER
    description: str = ""
    transaction_date: Optional[date] = None 

class TransactionUpdate(SQLModel):
    amount: Optional[float] = None
    category: Optional[TransactionCategory] = None
    description: Optional[str] = None
    transaction_date: Optional[date] = None 

class TransactionResponse(SQLModel):
    id: int
    user_id: int
    amount: float
    category: TransactionCategory
    description: str
    transaction_date: date
    created_at: datetime 

# -- Subscription -- 

class SubscriptionCreate(SQLModel):
    name: str
    amount: float
    billing_cycle: BillingCycle = BillingCycle.MONTHLY
    next_due: date
    active: bool = True 

class SubscriptionUpdate(SQLModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    billing_cycle: Optional[BillingCycle] = None
    next_due: Optional[date] = None
    active: Optional[bool] = None

class SubscriptionResponse(SQLModel):
    id: int
    user_id: int
    name: str
    amount: float
    billing_cycle: BillingCycle
    next_due: date
    active: bool
    created_at: datetime 

# -- Budget -- 

class BudgetCreate(SQLModel):
    category: TransactionCategory
    limit_amount: float
    period: BudgetPeriod = BudgetPeriod.MONTHLY

class BudgetUpdate(SQLModel):
    category: Optional[TransactionCategory] = None
    limit_amount: Optional[float] = None
    period: Optional[BudgetPeriod] = None 

class BudgetResponse(SQLModel):
    id: int
    user_id: int
    category: TransactionCategory
    limit_amount: float
    period: BudgetPeriod
    created_at: datetime

# -- Income -- 

class IncomeCreate(SQLModel):
    source: str
    amount: float
    income_date: Optional[date] = None
    is_recurring: bool = False
    recurrence_period: Optional[BudgetPeriod] = None

class IncomeUpdate(SQLModel):
    source: Optional[str] = None
    amount: Optional[float] = None
    income_date: Optional[date] = None
    is_recurring: Optional[bool] = None
    recurrence_period: Optional[BudgetPeriod] = None

class IncomeResponse(SQLModel):
    id: int
    user_id: int
    source: str
    amount: float
    income_date: date
    is_recurring: bool
    recurrence_period: Optional[BudgetPeriod]
    created_at: datetime 

# -- Reports -- 

class CategorySpend(SQLModel): 
    category: TransactionCategory
    total: float
    percentage: float 

class BurnRateReport(SQLModel):
    total_income: float
    total_expenses: float
    total_subscriptions: float
    net: float
    burn_rate_percentage: float
    category_breakdown: list[CategorySpend] 

class BudgetStatus(SQLModel):
    budget_id: int
    category: TransactionCategory
    limit_amount: float
    spent: float
    remaining: float
    over_budget: bool
