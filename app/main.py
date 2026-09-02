from fastapi import FastAPI

app = FastAPI(
    title="Python DevOps Time Tracking API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Python DevOps Time Tracking API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
