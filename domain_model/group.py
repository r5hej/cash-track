from typing import List
from domain_model.account import Account
from dataclasses import dataclass


@dataclass
class Group:
    id: int
    name: str
    accounts: List[Account]

