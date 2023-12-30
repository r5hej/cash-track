from typing import List, Optional

import persistence.db as db
from domain_model.account import Account
from domain_model.group import Group
from domain_model.group_protocols import GroupRepository
from .account import get_account_repository


class _Sqlite3GroupRepository(GroupRepository):
    """"""

    def __init__(self) -> None:
        super().__init__()
        db._init_db_if_not_yet()

    def create(self, name: str, accounts: List[Account] = []) -> Group:
        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute(
                "INSERT INTO groups VALUES (?)", (name,)
            )
            return Group(id=res.lastrowid, name=name, accounts=[])

    def delete(self, group: Group) -> None:
        with db.sqlite3_connection:
            db.sqlite3_connection.execute(
                "DELETE FROM groups WHERE rowid = :group_id", {"group_id": group.id}
            )

    def fetch_one(self, group_id: int) -> Optional[Group]:
        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute(
                "SELECT rowid, name FROM groups WHERE rowid = :group_id",
                {"group_id": group_id},
            )
            row_id, name = res.fetchone()
            if row_id is None:
                return None

            group = Group(id=row_id, name=name, accounts=[])
            account_repo = get_account_repository()
            for account in account_repo.fetch_in_group(group=group):
                group.accounts.append(account)
            return group

    def fetch_all(self) -> List[Group]:
        with db.sqlite3_connection:
            group_missing_accounts: List[Group] = []
            for rowid, name in db.sqlite3_connection.execute(
                "SELECT rowid, name FROM groups"
            ):
                group_missing_accounts.append(Group(id=rowid, name=name, accounts=[]))

            account_repo = get_account_repository()

            groups: List[Group] = []
            for group in group_missing_accounts:
                for account in account_repo.fetch_in_group(group=group):
                    group.accounts.append(account)
                groups.append(group)

            return groups

    def add_account(self, account: Account, group: Group) -> None:
        with db.sqlite3_connection:
            db.sqlite3_connection.execute(
                "INSERT INTO accounts_and_groups VALUES (:account_id, :group_id)",
                {"account_id": account.id, "group_id": group.id},
            )

    def remove_account(self, account: Account, group: Group) -> None:
        with db.sqlite3_connection:
            db.sqlite3_connection.execute(
                "DELETE FROM accounts_and_groups WHERE account_id = :account_id AND group_id = :group_id",
                {"account_id": account.id, "group_id": group.id},
            )

    def is_account_in_group(self, account: Account, group: Group) -> bool:
        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute(
                "SELECT rowid, account_id, group_id FROM accounts_and_groups WHERE account_id = :account_id AND group_id = :group_id",
                {"account_id": account.id, "group_id": group.id},
            )
            return res.fetchone() is not None


def get_group_repository() -> GroupRepository:
    return _Sqlite3GroupRepository()
