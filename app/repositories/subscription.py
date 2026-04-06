from sqlmodel import Session, select, func 
from app.models.finance import Subscription, BillingCycle 
from app.schemas.finance import SubscriptionCreate, SubscriptionUpdate 
from typing import Optional
import logging 

logging = logging.getLogger(__name__)

class SubscriptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, data: SubscriptionCreate) -> Subscription: 
        sub = Subscription(
            user_id=user_id,
            name=data.name,
            amount=data.amount,
            billing_cycle=data.billing_cycle,
            next_due=data.next_due,
            active=data.active 
        ) 
        try: 
            self.db.add(sub) 
            self.db.commit() 
            self.db.refresh(sub) 
            return sub
        except Exception as e:
            logging.error(f"Error creating subscription: {e}")
            self.db.rollback()
            raise 

    def get_by_id(self, sub_id: int, user_id: int) -> Optional[Subscription]:
        return self.db.exec(
            select(Subscription).where(Subscription.id == sub_id, Subscription.user_id == user_id)
        ).one_or_none()

    def get_all(self, user_id: int, active_only: bool = False) -> list[Subscription]:
        query = select(Subscription).where(Subscription.user_id == user_id)
        if active_only:
            query = query.where(Subscription.active == True)
        query = query.order_by(Subscription.next_due.asc())
        return list(self.db.exec(query).all())

    def update(self, sub: Subscription, data: SubscriptionUpdate) -> Subscription:
        if data.name is not None:
            sub.name = data.name
        if data.amount is not None:
            sub.amount = data.amount
        if data.billing_cycle is not None:
            sub.billing_cycle = data.billing_cycle
        if data.next_due is not None:
            sub.next_due = data.next_due
        if data.active is not None:
            sub.active = data.active
        try:
            self.db.add(sub)
            self.db.commit()
            self.db.refresh(sub)
            return sub
        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            self.db.rollback()
            raise

    def delete(self, sub: Subscription):
        try:
            self.db.delete(sub)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting subscription: {e}")
            self.db.rollback()
            raise

    def monthly_total(self, user_id: int) -> float:
        """Return total monthly cost of all active subscriptions, normalised to monthly."""
        subs = self.get_all(user_id, active_only=True)
        total = 0.0
        multipliers = {
            BillingCycle.WEEKLY: 4.33,
            BillingCycle.MONTHLY: 1,
            BillingCycle.QUARTERLY: 1 / 3,
            BillingCycle.YEARLY: 1 / 12,
        }
        for s in subs:
            total += s.amount * multipliers.get(s.billing_cycle, 1)
        return round(total, 2) 
