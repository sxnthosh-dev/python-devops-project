
import logging
from fastapi import FastAPI
from app.logging_config import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator
from app.api.users import router as users_router
from prometheus_fastapi_instrumentator import Instrumentator

setup_logging()
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Python DevOps Time Tracking API",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app)

app.include_router(users_router)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application started")

@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": "Python DevOps Time Tracking API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/version")
def version():
    return {"version": "1.0.2"}
