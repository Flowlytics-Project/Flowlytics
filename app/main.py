import uvicorn
from fastapi import FastAPI, Request, status
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from app.routers import templates, static_files, router, api_router
from app.config import get_settings
from contextlib import asynccontextmanager 


def _seed_users():
    from sqlmodel import Session, select
    from app.database import engine
    from app.models.user import User
    from app.utilities.security import encrypt_password 

    with Session(engine) as session: 
        existing = session.exec(select(User).where(User.username == "bob")).first()
        if not existing:
            bob = User(
                username="bob",
                email="bob@mail.com", 
                password=encrypt_password("bobpass"),
                role="admin",
            )
            session.add(bob)
            session.commit()
            print("Seeded user 'bob' with password 'bobpass'")
        else:
            print("User 'bob' already exists, skipping seeding.")

        existing = session.exec(select(User).where(User.username == "jon")).first()
        if not existing:
            jon = User(
                username="jon",
                email="jon@mail.com", 
                password=encrypt_password("jonpass"),
                role="admin",
            )
            session.add(jon)
            session.commit()
            print("Seeded user 'jon' with password 'bobpass'")
        else:
            print("User 'jon' already exists, skipping seeding.") 


@asynccontextmanager
async def lifespan(app: FastAPI): 
    import app.models 
    from app.database import create_db_and_tables
    create_db_and_tables()
    _seed_users()
    yield



app = FastAPI(
    middleware=[Middleware(SessionMiddleware, secret_key=get_settings().secret_key)],
    lifespan=lifespan,
    title="Flowlytics", 
    description="Personal Finance & Expense Tracker",
    version="1.0.0",
)   

app.include_router(router)
app.include_router(api_router)
app.mount("/static", static_files, name="static")

@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_redirect_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(
        request=request, 
        name="401.html",
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=get_settings().app_host, port=get_settings().app_port, reload=get_settings().env.lower()!="production")