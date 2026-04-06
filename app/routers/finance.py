from fastapi import Request, Query
from typing import Optional
from datatime import datetime, date
from . import api_router
from app.dependencies import SessionDep
from app.dependencies.auth import AuthDep 
from app.repositories.transaction import TransactionRepository
from app.repositories.subscription import SubscriptionRepository 
from app.repositories.budget import BudgetRepository
from app.repositories.income import IncomeRepository 
from  app.services.finance_service import FinanceService 
from app.schemas.finance import ( 
    TransactionCreate, TransactionUpdate, TransactionResponse,
    SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse,
    BudgetCreate, BudgetUpdate, BudgetResponse,
    IncomeCreate, IncomeUpdate, IncomeResponse,
    BurnRateReport, BudgetStatus,
) 
from app.models.finance import TransactionCategory 

def _get_service(db) -> FinanceService:
    return FinanceService(
        tx_repo=TransactionRepository(db),
        sub_repo=SubscriptionRepository(db),
        budget_repo=BudgetRepository(db),
        income_repo=IncomeRepository(db),
    ) 

# -- Transactions -- 

@api_router.post("/transactions", response_model=TransactionResponse, status_code=201, tags=["Transactions"]) 
async def create_transaction( data: TransactionCreate, user: AuthDep, db: SessionDep): 
     return _get_service(db).create_transaction(user.id, data) 

@api_router.get("/transactions", response_model=list[TransactionResponse], tags=["Transactions"])
async def list_transactions(
     user: AuthDep,
     db: SessionDep,
     category: Optional[TransactionCategory] = None,
     start_date: Optional[date] = None,
     end_date: Optional[date] = None,
): 
     return _get_service(db).list_transactions(user.id, category, start_date, end_date)


@api_router.get("/transactions/{tx_id}", response_model=TransactionResponse, tags=["Transactions"])
async def get_transaction(tx_id: int, user: AuthDep, db: SessionDep):
    return _get_service(db).get_transaction(user.id, tx_id)


@api_router.put("/transactions/{tx_id}", response_model=TransactionResponse, tags=["Transactions"])
async def update_transaction(tx_id: int, data: TransactionUpdate, user: AuthDep, db: SessionDep):
    return _get_service(db).update_transaction(user.id, tx_id, data)


@api_router.delete("/transactions/{tx_id}", status_code=204, tags=["Transactions"])
async def delete_transaction(tx_id: int, user: AuthDep, db: SessionDep):
    _get_service(db).delete_transaction(user.id, tx_id)


# -- Subscriptions -- 

@api_router.post("/subscriptions", response_model=SubscriptionResponse, status_code=201, tags=["Subscriptions"])
async def create_subscription(data: SubscriptionCreate, user: AuthDep, db: SessionDep):
    return _get_service(db).create_subscription(user.id, data)


@api_router.get("/subscriptions", response_model=list[SubscriptionResponse], tags=["Subscriptions"])
async def list_subscriptions(
    user: AuthDep,
    db: SessionDep,
    active_only: bool = False,
):
    return _get_service(db).list_subscriptions(user.id, active_only)


@api_router.get("/subscriptions/{sub_id}", response_model=SubscriptionResponse, tags=["Subscriptions"])
async def get_subscription(sub_id: int, user: AuthDep, db: SessionDep):
    return _get_service(db).get_subscription(user.id, sub_id)


@api_router.put("/subscriptions/{sub_id}", response_model=SubscriptionResponse, tags=["Subscriptions"])
async def update_subscription(sub_id: int, data: SubscriptionUpdate, user: AuthDep, db: SessionDep):
    return _get_service(db).update_subscription(user.id, sub_id, data)


@api_router.delete("/subscriptions/{sub_id}", status_code=204, tags=["Subscriptions"])
async def delete_subscription(sub_id: int, user: AuthDep, db: SessionDep):
    _get_service(db).delete_subscription(user.id, sub_id)


# -- Budgets --

@api_router.post("/budgets", response_model=BudgetResponse, status_code=201, tags=["Budgets"])
async def create_budget(data: BudgetCreate, user: AuthDep, db: SessionDep):
    return _get_service(db).create_budget(user.id, data)


@api_router.get("/budgets", response_model=list[BudgetResponse], tags=["Budgets"])
async def list_budgets(user: AuthDep, db: SessionDep):
    return _get_service(db).list_budgets(user.id)


@api_router.get("/budgets/{budget_id}", response_model=BudgetResponse, tags=["Budgets"])
async def get_budget(budget_id: int, user: AuthDep, db: SessionDep):
    return _get_service(db).get_budget(user.id, budget_id)


@api_router.put("/budgets/{budget_id}", response_model=BudgetResponse, tags=["Budgets"])
async def update_budget(budget_id: int, data: BudgetUpdate, user: AuthDep, db: SessionDep):
    return _get_service(db).update_budget(user.id, budget_id, data)


@api_router.delete("/budgets/{budget_id}", status_code=204, tags=["Budgets"])
async def delete_budget(budget_id: int, user: AuthDep, db: SessionDep):
    _get_service(db).delete_budget(user.id, budget_id)


# -- Incomes --

@api_router.post("/incomes", response_model=IncomeResponse, status_code=201, tags=["Incomes"])
async def create_income(data: IncomeCreate, user: AuthDep, db: SessionDep):
    return _get_service(db).create_income(user.id, data)


@api_router.get("/incomes", response_model=list[IncomeResponse], tags=["Incomes"])
async def list_incomes(
    user: AuthDep,
    db: SessionDep,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    return _get_service(db).list_incomes(user.id, start_date, end_date)


@api_router.get("/incomes/{income_id}", response_model=IncomeResponse, tags=["Incomes"])
async def get_income(income_id: int, user: AuthDep, db: SessionDep):
    return _get_service(db).get_income(user.id, income_id)


@api_router.put("/incomes/{income_id}", response_model=IncomeResponse, tags=["Incomes"])
async def update_income(income_id: int, data: IncomeUpdate, user: AuthDep, db: SessionDep):
    return _get_service(db).update_income(user.id, income_id, data)


@api_router.delete("/incomes/{income_id}", status_code=204, tags=["Incomes"])
async def delete_income(income_id: int, user: AuthDep, db: SessionDep):
    _get_service(db).delete_income(user.id, income_id)


# -- Reports -- 

@api_router.get("/reports/burn-rate", response_model=BurnRateReport, tags=["Reports"])
async def burn_rate(
    user: AuthDep,
    db: SessionDep,
    year: int = Query(default=datetime.now().year),
    month: int = Query(default=datetime.now().month, ge=1, le=12),
):
    return _get_service(db).get_burn_rate(user.id, year, month)


@api_router.get("/reports/budget-status", response_model=list[BudgetStatus], tags=["Reports"])
async def budget_status(
    user: AuthDep,
    db: SessionDep,
    year: int = Query(default=datetime.now().year),
    month: int = Query(default=datetime.now().month, ge=1, le=12),
):
    return _get_service(db).get_budget_status(user.id, year, month)
