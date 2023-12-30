from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel

import controllers.accounts

router = APIRouter(
    prefix="/account",
    tags=["Account"],
)


class AccountDTO(BaseModel):
    id: int
    name: str
    username: str


class CreateAccountDTO(BaseModel):
    name: str
    username: str


@router.get("")
def get_accounts(
    account_id: Optional[int] = None,
    name: Optional[str] = None,
    username: Optional[str] = None,
) -> List[AccountDTO]:
    response_body = []
    for account in controllers.accounts.get_accounts():
        response_body.append(
            AccountDTO(id=account.id, name=account.name, username=account.username)
        )
    return response_body


@router.post("", status_code=201)
def create_account(payload: CreateAccountDTO) -> None:
    controllers.accounts.create_account(name=payload.name, username=payload.username)
    return "Created account"


@router.delete("/{account_id}")
def delete_account(account_id: int) -> None:
    error = controllers.accounts.delete_account(account_id=account_id)
    if error is not None:
        return error.get_error()

    return "Deleted account"
