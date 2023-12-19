from typing import Protocol, Dict, Optional
from datetime import datetime
from domain_model.group import Group
from domain_model.account import Account
from dataclasses import dataclass


@dataclass
class Payment:
    id: int
    payee: Account
    createdAt: datetime
    distribution: Dict[int, int]
    message: str
    groupId: int = None


class PaymentFactory(Protocol):
    def create(
        self,
        payee: Account,
        group: Group,
        distribution: Dict[int, int] = {},
        message: Optional[str] = None,
    ) -> Payment:
        pass


class PaymentDistributionUpdater(Protocol):
    def update_distribution(self, payment: Payment, distribution: Dict[int, int]) -> None:
        pass


class PaymentDeletor(Protocol):
    def delete(self, payment: Payment) -> None:
        pass


class PaymentFetcher(Protocol):
    def fetch_one(self, id: int) -> Optional[Payment]:
        pass

    def fetch_all(self) -> [Payment]:
        pass


class PaymentRepository(
    PaymentFactory,
    PaymentDeletor,
    PaymentDistributionUpdater,
    PaymentFetcher,
    Protocol,
):
    """ """
