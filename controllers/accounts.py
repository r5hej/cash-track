from typing import Optional, List
from domain_model.account import Account
from domain_model.account_protocols import AccountNotFoundError
from domain_model.error import Error
from persistence.account import get_account_repository
import persistence.db as db


def get_accounts() -> List[Account]:
    repo = get_account_repository()
    accounts = repo.fetch_all()
    db.disconnect()
    return accounts


def create_account(name: str, username: str) -> None:
    repo = get_account_repository()
    account = repo.create(name=name, username=username)
    print(f"Created account {account}")
    db.disconnect()


def delete_account(account_id: int) -> Optional[Error]:
    repo = get_account_repository()
    account = repo.fetch_one(id=account_id)
    if account is None:
        return AccountNotFoundError(account_id=account_id)

    repo.delete(account)
    db.disconnect()
    return None
