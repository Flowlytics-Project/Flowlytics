import typer 
from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models.user import User
from app.utilities.security import encrypt_password

cli = typer.Typer() 

@cli.command() 
def init(): 
    create_db_and_tables() 
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