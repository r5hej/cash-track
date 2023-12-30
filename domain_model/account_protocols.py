from typing import Protocol, List, Optional
from .account import Account
from .error import Error
from .group import Group


class AccountFactory(Protocol):
    def create(self, name: str, username: str) -> Account:
        pass


class AccountDeletor(Protocol):
    def delete(self, user: Account) -> None:
        pass


class AccountFetcher(Protocol):
    def fetch_one(
        self, id: int = None, name: str = None, username: str = None
    ) -> Optional[Account]:
        pass

    def fetch_all(self) -> List[Account]:
        pass

    def fetch_in_group(self, group: Group) -> List[Account]:
        pass


class AccountRepository(AccountFactory, AccountFetcher, AccountDeletor, Protocol):
    """"""


class AccountNotFoundError(Error):
    def __init__(self, account_id: int = None) -> None:
        message = f"Coult not found account account. ID = {account_id}"
        super().__init__(message=message)
