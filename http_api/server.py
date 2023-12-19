from fastapi import FastAPI
from .router import accounts, groups, payments
import uvicorn

app = FastAPI()
app.include_router(accounts.router)
app.include_router(groups.router)
app.include_router(payments.router)



def init_server() -> None:
    uvicorn.run(app="http_api.server:app", log_level="info", reload=True)
