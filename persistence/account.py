from domain_model.account import Account
from domain_model.account_protocols import AccountRepository
from domain_model.group import Group
import persistence.db as db
from typing import Optional, List


class _Sqlite3AccountRepository(AccountRepository):
    """ """

    def __init__(self) -> None:
        super().__init__()
        db._init_db_if_not_yet()

    def create(self, name: str, username: str) -> Account:
        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute(
                "INSERT INTO accounts VALUES (:name, :username)", (name, username)
            )
            return Account(id=res.lastrowid, name=name, username=username)

    def delete(self, account: Account) -> None:
        with db.sqlite3_connection:
            db.sqlite3_connection.execute(
                "DELETE FROM accounts WHERE username=?", (account.username,)
            )

    def fetch_one(self, id: int = None, name: str = None, username: str = None) -> Optional[Account]:
        with db.sqlite3_connection:
            query = None
            if (id):
                query = 'SELECT rowid, name, username FROM accounts WHERE rowid = :id'
            elif (name):
                query = 'SELECT rowid, name, username FROM accounts WHERE name = :name'
            elif (username):
                query = 'SELECT rowid, name, username FROM accounts WHERE username = :username'
            else:
                raise Exception('Invalid input. Everything is None')
            for id, name, username in db.sqlite3_connection.execute(query, {'id': id, 'name': name, 'username': username}):
                return Account(id=id, name=name, username=username)
                
            

    def fetch_in_group(self, group: Group) -> List[Account]:
        with db.sqlite3_connection:
            query = 'SELECT a.rowid, a.name, a.username FROM accounts a join accounts_and_groups ag ON a.rowid = ag.account_id WHERE ag.group_id = :group_id'
            accounts: List[Account] = []
            for id, name, username in db.sqlite3_connection.execute(query, {'group_id': group.id}):
                accounts.append(Account(id=id, name=name, username=username))

            return accounts


    def fetch_all(self) -> List[Account]:
        with db.sqlite3_connection:
            users: List[Account] = []
            for id, name, username in db.sqlite3_connection.execute(
                "SELECT rowid, name, username FROM accounts"
            ):
                users.append(Account(id=id, name=name, username=username))
            return users


def get_account_repository() -> AccountRepository:
    return _Sqlite3AccountRepository()
