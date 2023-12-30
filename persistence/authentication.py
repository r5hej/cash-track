from datetime import datetime

import persistence.db as db
from domain_model.account import Account


class AuthRepository:
    def __init__(self) -> None:
        super().__init__()
        db._init_db_if_not_yet()

    def create_session(self, account: Account, token: str, expiry_time: datetime) -> None:
        with db.sqlite3_connection:
            db.sqlite3_connection.execute(
                "INSERT INTO login_session VALUES(:account_id, :token, :expiry_time)",
                {
                    "account_id": account.id,
                    "expiry_time": expiry_time.strftime("%m/%d/%Y"),
                    "token": token
                },
            )

    def delete_session(self, account: Account) -> None:
        with db.sqlite3_connection:
            db.sqlite3_connection.execute(
                "DELETE FROM login_session WHERE account_id = :account_id",
                {"account_id": account.id},
            )


def get_auth_repository() -> AuthRepository:
    return AuthRepository()
