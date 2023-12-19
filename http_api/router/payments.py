from typing import Optional, Dict, List
from fastapi import APIRouter
from pydantic import BaseModel


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


class CreatePaymentDTO(BaseModel):
    payee_id: int
    group_id: int
    created_at: str
    distribution: List[PaymentPayeeDTO]
    message: Optional[str] = None


@router.get("")
def get_payments(payment_id: Optional[int] = None) -> List[PaymentDTO]:
    raise Exception("Not implemented")


@router.post("", status_code=201)
def create_payment(payload: CreatePaymentDTO) -> None:
    raise Exception("Not implemented")


@router.delete("/{payment-id}")
def delete_payment(payment_id: int) -> None:
    raise Exception("Not implemented")
