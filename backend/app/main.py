from fastapi import FastAPI
from app.db import database, models
from app.api.v1.routes import auth
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import accounts
from app.api.v1.routes import admin

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SmartBank API", version="1.0")

origins = [
    "http://localhost:5173",
    # You can add more allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Welcome to SmartBank API"}
