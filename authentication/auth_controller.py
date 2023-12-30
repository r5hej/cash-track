import bcrypt
from uuid import uuid4
from typing import Optional, Tuple
from persistence.account import get_account_repository
from persistence.authentication import get_auth_repository
from datetime import datetime


def authenticate(username: str, password: str) -> Optional[Tuple[str, datetime]]:
    account_repo = get_account_repository()
    account = account_repo.fetch_one(username=username)
    if account is None:
        raise Exception(f'Could not finder account with username <{username}>')

    if not bcrypt.checkpw(str.encode(password), str.encode(account.password)):
        return None

    token = str(uuid4())
    expiry_time = datetime.now()
    auth_repo = get_auth_repository()
    auth_repo.delete_session(account=account)
    auth_repo.create_session(account=account, token=token, expiry_time=expiry_time)
    return token, expiry_time

