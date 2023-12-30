from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/tag",
    tags=["Tag"],
)


class TagDTO(BaseModel):
    id: int
    name: str


class CreateTagDTO(BaseModel):
    name: str


@router.get("")
def get_tags() -> List[TagDTO]:
    raise Exception("Not implemented")


@router.post("")
def create_tag(payload: CreateTagDTO) -> None:
    raise Exception("Not implemented")


@router.delete("/{tag_id}")
def delete_tag(tag_id: int) -> None:
    raise Exception("Not implemented")
