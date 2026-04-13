from fastapi import Request, Query, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from datetime import datetime, date
from . import api_router
import typer
from app.dependencies import SessionDep
from app.dependencies.auth import AuthDep 
from app.repositories.transaction import TransactionRepository
from app.repositories.subscription import SubscriptionRepository 
from app.repositories.budget import BudgetRepository
from app.repositories.income import IncomeRepository 
from  app.services.finance_service import FinanceService 
from . import templates
from app.schemas.finance import ( 
    TransactionCreate, TransactionUpdate, TransactionResponse,
    SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse,
    BudgetCreate, BudgetUpdate, BudgetResponse,
    IncomeCreate, IncomeUpdate, IncomeResponse,
    BurnRateReport, BudgetStatus, BillingCycle
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

@api_router.get("/transactions/create", response_class=HTMLResponse, status_code=201, tags=["Transactions"]) 
async def create_transaction(user: AuthDep, db: SessionDep, request: Request): 
     transactions = _get_service(db).list_transactions(user.id, category=None, start_date=None, end_date=None)
     selected_transaction = None
     form_action = "create"
     return templates.TemplateResponse(
        request=request, 
        name="transactions-form.html",
        context={
            "user": user,
            "transactions": transactions,
            "selected_transaction": selected_transaction,
            "form_action": form_action
        }
    )

@api_router.post("/transactions/create", response_model=TransactionResponse, status_code=201, tags=["Transactions"]) 
async def create_transaction(user: AuthDep, db: SessionDep, request: Request, amount_field: str = Form(), category_field: str = Form(), description_field: str = Form()): 
    if category_field == "food":
        category_field = TransactionCategory.FOOD
    elif category_field == "transport":
        category_field = TransactionCategory.TRANSPORT
    elif category_field == "housing":
        category_field = TransactionCategory.HOUSING
    elif category_field == "entertainment":
        category_field = TransactionCategory.ENTERTAINMENT
    elif category_field == "health":
        category_field = TransactionCategory.HEALTH
    elif category_field == "education":
        category_field = TransactionCategory.EDUCATION
    elif category_field == "clothing":
        category_field = TransactionCategory.CLOTHING
    elif category_field == "utilities":
        category_field = TransactionCategory.UTILITIES
    elif category_field == "other":
        category_field = TransactionCategory.OTHER
    data = TransactionCreate(amount=amount_field, category=category_field, description=description_field)
    check = _get_service(db).create_transaction(user.id, data) 
    if check:
        typer.echo("Transaction Created")
    return RedirectResponse(url=request.url_for('list_transactions'), status_code=status.HTTP_303_SEE_OTHER)
    

@api_router.get("/transactions", response_class=HTMLResponse, tags=["Transactions"])
async def list_transactions(
     user: AuthDep,
     request: Request,
     db: SessionDep,
     category: Optional[TransactionCategory] = None,
     start_date: Optional[date] = None,
     end_date: Optional[date] = None,
): 
    transactions = _get_service(db).list_transactions(user.id, category, start_date, end_date)
    selected_transaction = None
    return templates.TemplateResponse(
        request=request, 
        name="transactions.html",
        context={
            "user": user,
            "transactions": transactions,
            "selected_transaction": selected_transaction
        }
    )


@api_router.get("/transactions/{tx_id}", response_class=HTMLResponse, tags=["Transactions"])
async def get_transaction(tx_id: int, user: AuthDep, db: SessionDep, request: Request):
    transactions = _get_service(db).list_transactions(user.id, category=None, start_date=None, end_date=None)
    selected_transaction = _get_service(db).get_transaction(user.id, tx_id)
    return templates.TemplateResponse(
        request=request, 
        name="transactions.html",
        context={
            "user": user,
            "transactions": transactions,
            "selected_transaction": selected_transaction
        }
    )
    
@api_router.get("/transactions/update/{tx_id}", response_class=HTMLResponse, status_code=201, tags=["Transactions"]) 
async def update_transaction(user: AuthDep, tx_id: int, db: SessionDep, request: Request): 
     transactions = _get_service(db).list_transactions(user.id, category=None, start_date=None, end_date=None)
     selected_transaction = _get_service(db).get_transaction(user.id, tx_id)
     form_action = "update"
     return templates.TemplateResponse(
        request=request, 
        name="transactions-form.html",
        context={
            "user": user,
            "transactions": transactions,
            "selected_transaction": selected_transaction,
            "form_action": form_action
        }
    )

@api_router.post("/transactions/update/{tx_id}", response_model=TransactionResponse, tags=["Transactions"])
async def update_transaction(user: AuthDep, tx_id: int, db: SessionDep, request: Request, amount_field: str = Form(), category_field: str = Form(), description_field: str = Form()): 
    if category_field == "food":
        category_field = TransactionCategory.FOOD
    elif category_field == "transport":
        category_field = TransactionCategory.TRANSPORT
    elif category_field == "housing":
        category_field = TransactionCategory.HOUSING
    elif category_field == "entertainment":
        category_field = TransactionCategory.ENTERTAINMENT
    elif category_field == "health":
        category_field = TransactionCategory.HEALTH
    elif category_field == "education":
        category_field = TransactionCategory.EDUCATION
    elif category_field == "clothing":
        category_field = TransactionCategory.CLOTHING
    elif category_field == "utilities":
        category_field = TransactionCategory.UTILITIES
    elif category_field == "other":
        category_field = TransactionCategory.OTHER
    data = TransactionCreate(amount=amount_field, category=category_field, description=description_field)
    typer.echo("Updating transaction")
    check = _get_service(db).update_transaction(user.id, tx_id, data) 
    if check:
        typer.echo("Transaction Updated")
    else:
        typer.echo("Transaction not found")
    return RedirectResponse(url=request.url_for('list_transactions'), status_code=status.HTTP_303_SEE_OTHER)


@api_router.get("/transactions/delete/{tx_id}", status_code=204, tags=["Transactions"])
async def delete_transaction(tx_id: int, user: AuthDep, request: Request, db: SessionDep):
    _get_service(db).delete_transaction(user.id, tx_id)
    return RedirectResponse(url=request.url_for('list_transactions'), status_code=status.HTTP_303_SEE_OTHER)


# -- Subscriptions -- 

@api_router.get("/subscriptions/create", response_class=HTMLResponse, status_code=201, tags=["Subscriptions"])
async def create_subscription(user: AuthDep, db: SessionDep, request: Request, active_only: bool = False):
    subscriptions = _get_service(db).list_subscriptions(user.id, active_only)
    selected_subscription = None
    form_action = "create"
    return templates.TemplateResponse(
        request=request,
        name="subscriptions-form.html",
        context={
            "user": user,
            "subscriptions": subscriptions,
            "selected_subscription": selected_subscription,
            "form_action": form_action
        }
    )


@api_router.post("/subscriptions/create", response_model=SubscriptionResponse, status_code=201, tags=["Subscriptions"])
async def create_subscription(user: AuthDep, db: SessionDep, request: Request, name_field: str = Form(), amount_field: str = Form(), billing_cycle_field: str = Form(), next_due_field: date = Form()):
    if billing_cycle_field == "weekly":
        billying_cycle_field = BillingCycle.WEEKLY
    elif billing_cycle_field == "monthly":
        billying_cycle_field = BillingCycle.MONTHLY
    elif billing_cycle_field == "quarterly":
        billying_cycle_field = BillingCycle.QUARTERLY
    elif billing_cycle_field == "yearly":
        billying_cycle_field = BillingCycle.YEARLY
    data = SubscriptionCreate(name=name_field, amount=amount_field, billing_cycle=billing_cycle_field, next_due=next_due_field)
    check = _get_service(db).create_subscription(user.id, data)
    if check:
        typer.echo("Subscription Created")
    return RedirectResponse(url=request.url_for('list_subscriptions'), status_code=status.HTTP_303_SEE_OTHER)


@api_router.get("/subscriptions", response_class=HTMLResponse, tags=["Subscriptions"])
async def list_subscriptions(
    user: AuthDep,
    db: SessionDep,
    request: Request,
    active_only: bool = False,
):
    subscriptions = _get_service(db).list_subscriptions(user.id, active_only)
    selected_subscription = None
    return templates.TemplateResponse(
        request=request,
        name="subscriptions.html",
        context={
            "user": user,
            "subscriptions": subscriptions,
            "selected_subscription": selected_subscription
        }
    )


@api_router.get("/subscriptions/{sub_id}", response_class=HTMLResponse, tags=["Subscriptions"])
async def get_subscription(sub_id: int, user: AuthDep, request: Request, db: SessionDep, active_only = False):
    subscriptions = _get_service(db).list_subscriptions(user.id, active_only)
    selected_subscription = _get_service(db).get_subscription(user.id, sub_id)
    return templates.TemplateResponse(
        request=request, 
        name="subscriptions.html",
        context={
            "user": user,
            "subscriptions": subscriptions,
            "selected_subscription": selected_subscription
        }
    )

@api_router.get("/subscriptions/update/{sub_id}", response_class=HTMLResponse, status_code=201, tags=["Subscriptions"]) 
async def update_transaction(user: AuthDep, sub_id: int, db: SessionDep, request: Request, active_only = False): 
     subscriptions = _get_service(db).list_subscriptions(user.id, active_only)
     selected_subscription = _get_service(db).get_subscription(user.id, sub_id)
     form_action = "update"
     return templates.TemplateResponse(
        request=request, 
        name="subscriptions-form.html",
        context={
            "user": user,
            "subscriptions": subscriptions,
            "selected_subscription": selected_subscription,
            "form_action": form_action
        }
    )

@api_router.post("/subscriptions/update/{sub_id}", response_model=SubscriptionResponse, tags=["Subscriptions"])
async def update_subscription(user: AuthDep, sub_id: int, db: SessionDep, request: Request, name_field: str = Form(), amount_field: str = Form(), billing_cycle_field: str = Form(), next_due_field: date = Form(), active_field: bool = Form()): 
    if billing_cycle_field == "weekly":
        billying_cycle_field = BillingCycle.WEEKLY
    elif billing_cycle_field == "monthly":
        billying_cycle_field = BillingCycle.MONTHLY
    elif billing_cycle_field == "quarterly":
        billying_cycle_field = BillingCycle.QUARTERLY
    elif billing_cycle_field == "yearly":
        billying_cycle_field = BillingCycle.YEARLY
    data = SubscriptionCreate(name=name_field, amount=amount_field, billing_cycle=billing_cycle_field, next_due=next_due_field, active=active_field)
    typer.echo("Updating subscription")
    check = _get_service(db).update_subscription(user.id, sub_id, data) 
    if check:
        typer.echo("Subscription Updated")
    else:
        typer.echo("Subscription not found")
    return RedirectResponse(url=request.url_for('list_subscriptions'), status_code=status.HTTP_303_SEE_OTHER)

@api_router.get("/subscriptions/delete/{sub_id}", status_code=204, tags=["Subscriptions"])
async def delete_subscription(sub_id: int, user: AuthDep, request: Request, db: SessionDep):
    _get_service(db).delete_subscription(user.id, sub_id)
    return RedirectResponse(url=request.url_for('list_subscriptions'), status_code=status.HTTP_303_SEE_OTHER)

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
