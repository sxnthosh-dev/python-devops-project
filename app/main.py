import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.users import router as users_router
from app.logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI application started")
    yield
    logger.info("FastAPI application stopped")


app = FastAPI(
    title="Python DevOps Time Tracking API",
    version="1.0.0",
    lifespan=lifespan,
)


Instrumentator().instrument(app).expose(app)

app.include_router(users_router)


@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.get("/")
def root():
    return {"message": "Python DevOps Time Tracking API is running"}


@app.get("/version")
def version():
    return {"version": "1.0.2"}