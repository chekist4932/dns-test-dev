from fastapi import FastAPI

from src.sales.router import router as router_sales
from src.exceptions import register_exception_handlers

app = FastAPI(title='dns-test-dev')
register_exception_handlers(app)

app.include_router(router_sales)
