from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel
from .accounts import AccountDTO
import controllers.groups


router = APIRouter(
    prefix="/group",
    tags=["Group"],
)


class GroupDTO(BaseModel):
    id: int
    name: str
    accounts: List[AccountDTO]


class CreateGroupDTO(BaseModel):
    name: str


@router.get("")
def get_groups(group_id: Optional[int] = None) -> List[GroupDTO]:
    response_body: List[GroupDTO] = []
    for group in controllers.groups.get_groups(group_id=group_id):
        accounts: List[AccountDTO] = [
            AccountDTO(id=account.id, name=account.name, username=account.username)
            for account in group.accounts
        ]

        response_body.append(GroupDTO(id=group.id, name=group.name, accounts=accounts))

    return response_body


@router.post("", status_code=201)
def create_group(payload: CreateGroupDTO) -> None:
    controllers.groups.create_group(name=payload.name)
    return "Group created"


@router.delete("/{group_id}")
def delete_group(group_id: int) -> None:
    controllers.groups.delete_group(group_id=group_id)
    return "Group deleted"


@router.put("/{group_id}/account/{account_id}/add")
def add_account_to_group(group_id: int, account_id: int) -> None:
    controllers.groups.add_account_to_group(group_id=group_id, account_id=account_id)
    return "Added account to group"


@router.put("/{group_id}/account/{account_id}/remove")
def remove_account_from_group(group_id: int, account_id: int) -> None:
    controllers.groups.remove_account_to_group(group_id=group_id, account_id=account_id)
    return "Removed account to group"
