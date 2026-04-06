from sqlmodel import Session, select 
from app.models.finance import Budget, TransactionCategory 
from app.schemas.finance import BudgetCreate, BudgetUpdate
from typing import Optional 
import logging 

logger = logging.getLogger(__name__) 

class BudgetRepository: 
    def __init__(self, db: Session): 
        self.db = db 

    def create(self, user_id: int, data: BudgetCreate) -> Budget: 
        budget = Budget(
            user_id=user_id, 
            category=data.category, 
            limit_amount=data.limit_amount,
            period=data.period,
        ) 

        try: 
            self.db.add(budget) 
            self.db.commit() 
            self.db.refresh(budget) 
            return budget
        except Exception as e:
            logger.error(f"Error creating budget: {e}") 
            self.db.rollback() 
            raise 
    
    def get_by_id(self, budget_id: int, user_id: int) -> Optional[Budget]: 
        return self.db.exec(
            select(Budget).where(Budget.id == budget_id, Budget.user_id == user_id)
        ).one_or_none() 
    
    def get_all(self, user_id: int) -> list[Budget]: 
        return list(self.db.exec(select(Budget).where(Budget.user_id == user_id)).all()) 
    
    def get_by_category(self, user_id: int, category: TransactionCategory) -> Optional[Budget]: 
        return self.db.exec( 
            select(Budget).where(Budget.user_id == user_id, Budget.category == category)
        ).one_or_none() 
    
    def update(self, budget: Budget, data: BudgetUpdate) -> Budget: 
        if data.category is not None: 
            budget.category = data.category 
        if data.limit_amount is not None: 
            budget.limit_amount = data.limit_amount 
        if data.period is not None: 
            budget.period = data.period 

        try: 
            self.db.add(budget) 
            self.db.commit() 
            self.db.refresh(budget) 
            return budget
        except Exception as e:
            logger.error(f"Error updating budget: {e}") 
            self.db.rollback() 
            raise 

    def delete(self, budget: Budget): 
        try: 
            self.db.delete(budget) 
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting budget: {e}") 
            self.db.rollback() 
            raise 
         