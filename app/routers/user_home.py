from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from . import router, templates
from app.services.finance_service import FinanceService 
from app.repositories.transaction import TransactionRepository
from app.repositories.subscription import SubscriptionRepository 
from app.repositories.budget import BudgetRepository
from app.repositories.income import IncomeRepository

def _get_service(db) -> FinanceService:
    return FinanceService(
        tx_repo=TransactionRepository(db),
        sub_repo=SubscriptionRepository(db),
        budget_repo=BudgetRepository(db),
        income_repo=IncomeRepository(db),
    ) 

@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    transactions = _get_service(db).list_transactions(user.id)
    transactions = reversed(transactions)
    return templates.TemplateResponse(
        request=request, 
        name="home.html",
        context={
            "user": user,
            "transactions": transactions
        }
    )