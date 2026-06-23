from fastapi import FastAPI

from app.api.middlewares.correlation import CorrelationIdMiddleware
from app.api.routes.cv import router as cv_router
from app.core.logger import configure_logging

configure_logging()


app = FastAPI(
    title="CV Optimization Service",
    version="1.0.0",
)

app.add_middleware(CorrelationIdMiddleware)
app.include_router(cv_router)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
