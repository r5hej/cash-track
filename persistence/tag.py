from typing import List, Optional

import persistence.db as db
from domain_model.tag import TagRepository, Tag


class _Sqlite3TagRepository(TagRepository):
    def __init__(self) -> None:
        super().__init__()
        db._init_db_if_not_yet()

    def create(self, name: str) -> Tag:
        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute(
                "INSERT INTO tags VALUES (:name)", {"name": name}
            )
            return Tag(id=res.lastrowid, name=name)

    def fetch_one(self, tag_id: int) -> Optional[Tag]:
        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute(
                "SELECT rowid, name FROM tags WHERE rowid = :tag_id", {"tag_id": tag_id}
            )
            row_id, name = res.fetchone()
            if row_id is None:
                return None

            return Tag(id=row_id, name=name)

    def fetch_all(self) -> List[Tag]:
        with db.sqlite3_connection:
            tags: List[Tag] = []
            for row_id, name in db.sqlite3_connection.execute(
                "SELECT rowid, name FROM tags"
            ):
                tags.append(Tag(id=row_id, name=name))
            return tags

    def fetch_by_payment(self, payment_id: int) -> List[Tag]:
        with db.sqlite3_connection:
            tags: List[Tag] = []
            for row_id, name in db.sqlite3_connection.execute(
                "SELECT t.rowid, t.name FROM tags t JOIN tags_and_payments tp ON t.rowid = tp.tag_id WHERE tp.payment_id = :payment_id",
                {"payment_id": payment_id},
            ):
                tags.append(Tag(id=row_id, name=name))
            return tags


def get_tag_repository() -> TagRepository:
    return _Sqlite3TagRepository()
