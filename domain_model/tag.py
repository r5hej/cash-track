from dataclasses import dataclass
from typing import Protocol, List, Optional


@dataclass
class Tag:
    id: int
    name: str


class TagFactory(Protocol):
    def create(self, name: str) -> Tag:
        pass


class TagFetcher(Protocol):
    def fetch_one(self, tag_id: int) -> Optional[Tag]:
        pass

    def fetch_by_payment(self, payment_id: int) -> List[Tag]:
        pass

    def fetch_all(self) -> List[Tag]:
        pass


class TagRepository(TagFactory, TagFetcher, Protocol):
    """"""
