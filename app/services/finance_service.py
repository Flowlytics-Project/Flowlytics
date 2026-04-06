from fastapi import HTTPException, status
from app.repositories.transaction import TransactionRepository
from app.repositories.subscription import SubscriptionRepository
from app.repositories.budget import BudgetRepository
from app.repositories.income import IncomeRepository
from app.schemas.finance import (
    TransactionCreate, TransactionUpdate, TransactionResponse,
    SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse,
    BudgetCreate, BudgetUpdate, BudgetResponse,
    IncomeCreate, IncomeUpdate, IncomeResponse,
    BurnRateReport, CategorySpend, BudgetStatus,
)
from app.models.finance import TransactionCategory
from typing import Optional
from datetime import date, datetime, timezone
import calendar


def _not_found(resource: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource} not found")


class FinanceService:
    def __init__(
        self,
        tx_repo: TransactionRepository,
        sub_repo: SubscriptionRepository,
        budget_repo: BudgetRepository,
        income_repo: IncomeRepository,
    ):
        self.tx_repo = tx_repo
        self.sub_repo = sub_repo
        self.budget_repo = budget_repo
        self.income_repo = income_repo

    # -- Transactions -- 

    def create_transaction(self, user_id: int, data: TransactionCreate) -> TransactionResponse:
        tx = self.tx_repo.create(user_id, data)
        return TransactionResponse.model_validate(tx)

    def list_transactions(
        self,
        user_id: int,
        category: Optional[TransactionCategory] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[TransactionResponse]:
        txs = self.tx_repo.get_all(user_id, category, start_date, end_date)
        return [TransactionResponse.model_validate(t) for t in txs]

    def get_transaction(self, user_id: int, tx_id: int) -> TransactionResponse:
        tx = self.tx_repo.get_by_id(tx_id, user_id)
        if not tx:
            _not_found("Transaction")
        return TransactionResponse.model_validate(tx)

    def update_transaction(self, user_id: int, tx_id: int, data: TransactionUpdate) -> TransactionResponse:
        tx = self.tx_repo.get_by_id(tx_id, user_id)
        if not tx:
            _not_found("Transaction")
        updated = self.tx_repo.update(tx, data)
        return TransactionResponse.model_validate(updated)

    def delete_transaction(self, user_id: int, tx_id: int):
        tx = self.tx_repo.get_by_id(tx_id, user_id)
        if not tx:
            _not_found("Transaction")
        self.tx_repo.delete(tx)

    # -- Subscriptions -- 

    def create_subscription(self, user_id: int, data: SubscriptionCreate) -> SubscriptionResponse:
        sub = self.sub_repo.create(user_id, data)
        return SubscriptionResponse.model_validate(sub)

    def list_subscriptions(self, user_id: int, active_only: bool = False) -> list[SubscriptionResponse]:
        subs = self.sub_repo.get_all(user_id, active_only)
        return [SubscriptionResponse.model_validate(s) for s in subs]

    def get_subscription(self, user_id: int, sub_id: int) -> SubscriptionResponse:
        sub = self.sub_repo.get_by_id(sub_id, user_id)
        if not sub:
            _not_found("Subscription")
        return SubscriptionResponse.model_validate(sub)

    def update_subscription(self, user_id: int, sub_id: int, data: SubscriptionUpdate) -> SubscriptionResponse:
        sub = self.sub_repo.get_by_id(sub_id, user_id)
        if not sub:
            _not_found("Subscription")
        updated = self.sub_repo.update(sub, data)
        return SubscriptionResponse.model_validate(updated)

    def delete_subscription(self, user_id: int, sub_id: int):
        sub = self.sub_repo.get_by_id(sub_id, user_id)
        if not sub:
            _not_found("Subscription")
        self.sub_repo.delete(sub)

    # -- Budgets -- 

    def create_budget(self, user_id: int, data: BudgetCreate) -> BudgetResponse:
        budget = self.budget_repo.create(user_id, data)
        return BudgetResponse.model_validate(budget)

    def list_budgets(self, user_id: int) -> list[BudgetResponse]:
        budgets = self.budget_repo.get_all(user_id)
        return [BudgetResponse.model_validate(b) for b in budgets]

    def get_budget(self, user_id: int, budget_id: int) -> BudgetResponse:
        budget = self.budget_repo.get_by_id(budget_id, user_id)
        if not budget:
            _not_found("Budget")
        return BudgetResponse.model_validate(budget)

    def update_budget(self, user_id: int, budget_id: int, data: BudgetUpdate) -> BudgetResponse:
        budget = self.budget_repo.get_by_id(budget_id, user_id)
        if not budget:
            _not_found("Budget")
        updated = self.budget_repo.update(budget, data)
        return BudgetResponse.model_validate(updated)

    def delete_budget(self, user_id: int, budget_id: int):
        budget = self.budget_repo.get_by_id(budget_id, user_id)
        if not budget:
            _not_found("Budget")
        self.budget_repo.delete(budget)

    # -- Incomes -- 

    def create_income(self, user_id: int, data: IncomeCreate) -> IncomeResponse:
        income = self.income_repo.create(user_id, data)
        return IncomeResponse.model_validate(income)

    def list_incomes(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[IncomeResponse]:
        incomes = self.income_repo.get_all(user_id, start_date, end_date)
        return [IncomeResponse.model_validate(i) for i in incomes]

    def get_income(self, user_id: int, income_id: int) -> IncomeResponse:
        income = self.income_repo.get_by_id(income_id, user_id)
        if not income:
            _not_found("Income")
        return IncomeResponse.model_validate(income)

    def update_income(self, user_id: int, income_id: int, data: IncomeUpdate) -> IncomeResponse:
        income = self.income_repo.get_by_id(income_id, user_id)
        if not income:
            _not_found("Income")
        updated = self.income_repo.update(income, data)
        return IncomeResponse.model_validate(updated)

    def delete_income(self, user_id: int, income_id: int):
        income = self.income_repo.get_by_id(income_id, user_id)
        if not income:
            _not_found("Income")
        self.income_repo.delete(income)

    # -- Reports -- 

    def get_burn_rate(self, user_id: int, year: int, month: int) -> BurnRateReport:
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])

        total_income = self.income_repo.total_income(user_id, first_day, last_day)
        total_expenses = self.tx_repo.total_expenses(user_id, first_day, last_day)
        monthly_subs = self.sub_repo.monthly_total(user_id)

        total_out = total_expenses + monthly_subs
        net = total_income - total_out
        burn_pct = round((total_out / total_income * 100) if total_income > 0 else 0, 2)

        # Category breakdown
        by_cat = self.tx_repo.total_by_category(user_id, first_day, last_day)
        breakdown = []
        for cat, cat_total in by_cat:
            pct = round((cat_total / total_out * 100) if total_out > 0 else 0, 2)
            breakdown.append(CategorySpend(category=cat, total=round(cat_total, 2), percentage=pct))

        return BurnRateReport(
            total_income=round(total_income, 2),
            total_expenses=round(total_expenses, 2),
            total_subscriptions=monthly_subs,
            net=round(net, 2),
            burn_rate_percentage=burn_pct,
            category_breakdown=breakdown,
        )

    def get_budget_status(self, user_id: int, year: int, month: int) -> list[BudgetStatus]:
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])

        budgets = self.budget_repo.get_all(user_id)
        by_cat = {cat: total for cat, total in self.tx_repo.total_by_category(user_id, first_day, last_day)}

        statuses = []
        for b in budgets:
            spent = by_cat.get(b.category, 0.0)
            remaining = b.limit_amount - spent
            statuses.append(BudgetStatus(
                budget_id=b.id,
                category=b.category,
                limit_amount=b.limit_amount,
                spent=round(spent, 2),
                remaining=round(remaining, 2),
                over_budget=remaining < 0,
            ))
        return statuses
