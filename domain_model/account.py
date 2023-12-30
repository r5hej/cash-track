from dataclasses import dataclass


@dataclass
class Account:
    id: int
    name: str
    username: str
    password: str
