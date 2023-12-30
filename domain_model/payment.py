from datetime import datetime
from typing import Protocol, Dict, Optional, List

from domain_model.account import Account
from domain_model.group import Group
from domain_model.tag import Tag


class Payment:
    id: int
    payee: Account
    created_at: datetime
    distribution: Dict[int, int]
    message: Optional[str]
    group: Group
    tags: List[Tag]

    def __init__(
        self,
        id: int,
        payee: Account,
        group: Group,
        created_at: datetime,
        distribution: Dict[int, int],
        message: str = None,
        tags: List[Tag] = [],
    ):
        self.id = id
        self.payee = payee
        self.group = group
        self.created_at = created_at
        self.distribution = distribution
        self.message = message
        self.tags = tags


class PaymentFactory(Protocol):
    def create(
        self,
        payee: Account,
        group: Group,
        distribution: Dict[int, int] = {},
        message: Optional[str] = None,
        tags: List[Tag] = [],
    ) -> Payment:
        pass


class PaymentDistributionUpdater(Protocol):
    def update_distribution(
        self, payment: Payment, distribution: Dict[int, int]
    ) -> None:
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
