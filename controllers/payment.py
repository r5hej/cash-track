from typing import List, Optional, Dict

from domain_model.payment import Payment
from domain_model.tag import Tag
from persistence.account import get_account_repository
from persistence.group import get_group_repository
from persistence.payment import get_payment_repository


def get_payments(payment_id: Optional[int] = None) -> List[Payment]:
    payment_repo = get_payment_repository()

    if payment_id is None:
        return payment_repo.fetch_all()

    payment = payment_repo.fetch_one(id=payment_id)
    return [] if payment is None else [payment]


def create_payment(
    payee_id: int,
    group_id: int,
    distribution: Dict[int, int],
    message: Optional[str] = None,
    tags: List[Tag] = [],
) -> Payment:
    payment_repo = get_payment_repository()
    account_repo = get_account_repository()
    group_repo = get_group_repository()

    payee = account_repo.fetch_one(id=payee_id)
    if payee is None:
        raise Exception(f"could not find payee by id <{payee_id}>")

    group = group_repo.fetch_one(group_id=group_id)
    if group is None:
        raise Exception(f"could not find group by id <{group_id}>")

    return payment_repo.create(
        payee=payee, group=group, distribution=distribution, message=message, tags=tags
    )


def delete_payment(payment_id: int) -> None:
    repo = get_payment_repository()
    payment = repo.fetch_one(id=payment_id)
    if payment is None:
        return

    repo.delete(payment=payment)
