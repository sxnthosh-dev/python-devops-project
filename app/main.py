from fastapi import FastAPI

from app.api.users import router as users_router

app = FastAPI(
    title="Python DevOps Time Tracking API",
    version="1.0.0",
)

app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Python DevOps Time Tracking API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}