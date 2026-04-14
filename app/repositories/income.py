from sqlmodel import Session, select, func 
from app.models.finance import Income 
from app.schemas.finance import IncomeCreate, IncomeUpdate
from typing import Optional
from datetime import date 
import logging 

logger = logging.getLogger(__name__) 

class IncomeRepository:
    def __init__(self, db: Session): 
        self.db = db

    def create(self, user_id: int, data: IncomeCreate) -> Income: 
        income = Income(
            user_id=user_id,
            source=data.source,
            amount=data.amount, 
            income_date=data.income_date or date.today(), 
            is_recurring=data.is_recurring, 
            recurrence_period=data.recurrence_period,
        ) 
        try:
            self.db.add(income) 
            self.db.commit() 
            self.db.refresh(income) 
            return income
        except Exception as e:
            logger.error(f"Error creating income: {e}") 
            self.db.rollback() 
            raise 

    def get_by_id(self, income_id: int, user_id: int ) -> Optional[Income]: 
        return self.db.exec(
            select(Income).where(Income.id == income_id, Income.user_id == user_id) 
        ).one_or_none() 
        
    def get_all(self, user_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None,) -> list[Income]: 
        query = select(Income).where(Income.user_id == user_id) 
        if start_date: 
            query = query.where(Income.income_date >= start_date) 
        if end_date: 
            query = query.where(Income.income_date <= end_date) 
        query = query.order_by(Income.income_date.desc())
        return list(self.db.exec(query).all())
   
    def update(self, income: Income, data: IncomeUpdate) -> Income:
        if data.source is not None:
            income.source = data.source
        if data.amount is not None:
            income.amount = data.amount
        if data.income_date is not None:
            income.income_date = data.income_date
        if data.is_recurring is not None:
            income.is_recurring = data.is_recurring
        income.recurrence_period = data.recurrence_period
        try:
            self.db.add(income)
            self.db.commit()
            self.db.refresh(income)
            return income
        except Exception as e:
            logger.error(f"Error updating income: {e}")
            self.db.rollback()
            raise

    def delete(self, income: Income):
        try:
            self.db.delete(income)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting income: {e}")
            self.db.rollback()
            raise

    def total_income(self, user_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None) -> float:
        query = select(func.sum(Income.amount)).where(Income.user_id == user_id)
        if start_date:
            query = query.where(Income.income_date >= start_date)
        if end_date:
            query = query.where(Income.income_date <= end_date)
        result = self.db.exec(query).one_or_none()
        return float(result or 0)

