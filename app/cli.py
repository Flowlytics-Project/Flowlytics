import typer 
from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models.user import User
from app.models.finance import Transaction, TransactionCategory
from app.utilities.security import encrypt_password

cli = typer.Typer() 

@cli.command() 
def init(): 
    import app.models

    create_db_and_tables() 

    with Session(engine) as session:

        tx1 = Transaction(
            user_id=1,
            amount=100.0,
            category=TransactionCategory.ENTERTAINMENT,
            description="Movie"
        )

        session.add(tx1)

        tx0 = Transaction(
            user_id=1,
            amount=90.0,
            category=TransactionCategory.HEALTH,
            description="Panadol"
        )

        session.add(tx0)

        tx2 = Transaction(
            user_id=1,
            amount=80.0,
            category=TransactionCategory.CLOTHING,
            description="Hoodie"
        )

        session.add(tx2)

        tx3 = Transaction(
            user_id=1,
            amount=70.0,
            category=TransactionCategory.HOUSING,
            description="Paint"
        )

        session.add(tx3)

        session.commit()

        typer.echo("Tables created") 

@cli.command() 
def seed(): 
    with Session(engine) as session:
        existing = session.exec(
            select(User).where(User.username == "bob")
        ).first() 

        if existing: 
            typer.echo(" Bob already exists, skipping.")
            return
        
        bob = User(
            username="bob",
            email="bob@mail.com",
            password=encrypt_password("bobpass"),
            role="admin"
        ) 

        session.add(bob)

        session.commit()
        typer.echo("Seeded: bob / bobpass (admin)")

if __name__ == "__main__": 
    cli() 