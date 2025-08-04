from fastapi import FastAPI

from dataseed.api.routes import auth, management, transaction, users

app = FastAPI()
app.include_router(management.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transaction.router)
