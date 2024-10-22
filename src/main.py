from fastapi import FastAPI

from src.sales.router import router as router_sales

app = FastAPI(title='dns-test-dev')

app.include_router(router_sales)
