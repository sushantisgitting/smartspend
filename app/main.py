from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db
from app.routes import auth, users, accounts, categories, operations

app = FastAPI(
    title="Budget App",
    description="Project for BakAI practice week",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(operations.router)

@app.get("/")
def root():
    return {"message": "Budget App", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}