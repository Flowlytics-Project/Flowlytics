from sqlmodel import Session, select, func
from app.models.finance import Transaction, TransactionCategory
from app.schemas.finance import TransactionCreate, TransactionUpdate
from typing import Optional
from datetime import date
import logging

logger = logging.getLogger(__name__)


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, data: TransactionCreate) -> Transaction:
        tx = Transaction(
            user_id=user_id,
            amount=data.amount,
            category=data.category,
            description=data.description,
            transaction_date=data.transaction_date or date.today(),
        )
        try:
            self.db.add(tx)
            self.db.commit()
            self.db.refresh(tx)
            return tx
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, tx_id: int, user_id: int) -> Optional[Transaction]:
        return self.db.exec(
            select(Transaction).where(Transaction.id == tx_id, Transaction.user_id == user_id)
        ).one_or_none()

    def get_all(
        self,
        user_id: int,
        category: Optional[TransactionCategory] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[Transaction]:
        query = select(Transaction).where(Transaction.user_id == user_id)
        if category:
            query = query.where(Transaction.category == category)
        if start_date:
            query = query.where(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.where(Transaction.transaction_date <= end_date)
        query = query.order_by(Transaction.transaction_date.desc())
        return list(self.db.exec(query).all())

    def update(self, tx: Transaction, data: TransactionUpdate) -> Transaction:
        if data.amount is not None:
            tx.amount = data.amount
        if data.category is not None:
            tx.category = data.category
        if data.description is not None:
            tx.description = data.description
        if data.transaction_date is not None:
            tx.transaction_date = data.transaction_date
        try:
            self.db.add(tx)
            self.db.commit()
            self.db.refresh(tx)
            return tx
        except Exception as e:
            logger.error(f"Error updating transaction: {e}")
            self.db.rollback()
            raise

    def delete(self, tx: Transaction):
        try:
            self.db.delete(tx)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting transaction: {e}")
            self.db.rollback()
            raise

    def total_by_category(self, user_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None):
        query = (
            select(Transaction.category, func.sum(Transaction.amount).label("total"))
            .where(Transaction.user_id == user_id)
            .group_by(Transaction.category)
        )
        if start_date:
            query = query.where(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.where(Transaction.transaction_date <= end_date)
        return self.db.exec(query).all()

    def total_expenses(self, user_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None) -> float:
        query = select(func.sum(Transaction.amount)).where(Transaction.user_id == user_id)
        if start_date:
            query = query.where(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.where(Transaction.transaction_date <= end_date)
        result = self.db.exec(query).one_or_none()
        return float(result or 0)
