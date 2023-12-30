from typing import Optional, List, Dict

from fastapi import APIRouter
from pydantic import BaseModel
from http_api.router.tags import TagDTO

import controllers.payment

router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)


class PaymentPayeeDTO(BaseModel):
    account_id: int
    amount: int


class PaymentDTO(BaseModel):
    id: int
    payee_id: int
    group_id: int
    created_at: str
    distribution: List[PaymentPayeeDTO]
    message: Optional[str] = None
    tags: List[TagDTO] = []


class CreatePaymentDTO(BaseModel):
    payee_id: int
    group_id: int
    distribution: List[PaymentPayeeDTO]
    message: Optional[str] = None
    tags: List[TagDTO] = []


@router.get("")
def get_payments(payment_id: Optional[int] = None) -> List[PaymentDTO]:
    response_body: List[PaymentDTO] = []
    for payment in controllers.payment.get_payments(payment_id=payment_id):
        dto = PaymentDTO(
            id=payment.id,
            payee_id=payment.payee.id,
            group_id=payment.group.id,
            created_at=payment.created_at.strftime("%m/%d/%Y"),
            message=payment.message,
            distribution=[],
            tags=[TagDTO(id=tag.id, name=tag.name) for tag in payment.tags],
        )
        for payee_id, amount in payment.distribution.items():
            dto.distribution.append(PaymentPayeeDTO(account_id=payee_id, amount=amount))
        response_body.append(dto)

    return response_body


@router.post("", status_code=201)
def create_payment(payload: CreatePaymentDTO) -> None:
    distribution: Dict[int, int] = {
        dto.account_id: dto.amount for dto in payload.distribution
    }
    controllers.payment.create_payment(
        payee_id=payload.payee_id,
        group_id=payload.group_id,
        message=payload.message,
        distribution=distribution,
        tags=payload.tags,
    )


@router.delete("/{payment_id}")
def delete_payment(payment_id: int) -> None:
    controllers.payment.delete_payment(payment_id=payment_id)
