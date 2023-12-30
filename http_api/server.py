import uvicorn
from fastapi import FastAPI

from http_api.router import accounts, groups, payments, tags, authentication

app = FastAPI()
app.include_router(accounts.router)
app.include_router(groups.router)
app.include_router(payments.router)
app.include_router(tags.router)
app.include_router(authentication.router)


def init_server() -> None:
    uvicorn.run(app="http_api.server:app", log_level="info", reload=True)
