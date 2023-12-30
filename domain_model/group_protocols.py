from typing import Protocol, List, Optional
from .account import Account
from .group import Group


class GroupFactory(Protocol):
    def create(self, name: str, accounts: List[Account] = []) -> Group:
        pass


class GroupDeletor(Protocol):
    def delete(self, group: Group) -> None:
        pass


class GroupFetcher(Protocol):
    def fetch_one(self, group_id: int) -> Optional[Group]:
        pass

    def fetch_all(self) -> List[Group]:
        pass


class GroupAccountHandle(Protocol):
    def add_account(self, account: Account, group: Group) -> None:
        pass

    def remove_account(self, account: Account, group: Group) -> None:
        pass

    def is_account_in_group(self, account: Account, group: Group) -> bool:
        pass


class GroupRepository(
    GroupFactory,
    GroupDeletor,
    GroupFetcher,
    GroupAccountHandle,
    Protocol,
):
    """ """
