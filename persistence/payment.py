import datetime
import json
from typing import Optional, Dict, List

import persistence.db as db
from domain_model.account import Account
from domain_model.group import Group
from domain_model.payment import PaymentRepository, Payment
from domain_model.tag import Tag
from persistence.account import get_account_repository
from persistence.group import get_group_repository
from persistence.tag import get_tag_repository


class _Sqlite3PaymentRepository(PaymentRepository):
    def __init__(self) -> None:
        super().__init__()
        db._init_db_if_not_yet()

    def create(
        self,
        payee: Account,
        group: Group,
        distribution: Dict[Account, int] = {},
        message: Optional[str] = None,
        tags: List[Tag] = [],
    ) -> Payment:
        created_at = datetime.datetime.now()
        data = {
            "payee_id": payee.id,
            "group_id": group.id,
            "distribution": json.dumps(distribution),
            "created_at": created_at.strftime("%d/%m/%Y"),
        }
        if message is not None:
            data["message"] = message

        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute(
                "INSERT INTO payments VALUES (:payee_id, :group_id, :created_at, :distribution, :message)",
                data,
            )
            if len(tags) > 0:
                db.sqlite3_connection.executemany(
                    "INSERT INTO tags_and_payments VALUES (:tag_id, :payment_id)",
                    [{"tag_id": tag.id, "payment_id": res.lastrowid} for tag in tags],
                )
            return Payment(
                id=res.lastrowid,
                payee=payee,
                group=group,
                created_at=created_at,
                distribution=distribution,
                tags=tags,
                message=message,
            )

    def update_distribution(
        self, payment: Payment, distribution: Dict[Account, int]
    ) -> None:
        raise Exception("Not implemented")

    def delete(self, payment: Payment) -> None:
        with db.sqlite3_connection:
            db.sqlite3_connection.execute(
                "DELETE FROM payments where rowid = :payment_id",
                {"payment_id": payment.id},
            )

    def fetch_one(self, id: int) -> Optional[Payment]:
        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute(
                "SELECT rowid, payee_id, group_id, created_at, distribution, message FROM payments WHERE rowid = :payment_id",
                {"payment_id": id},
            )
            (
                rowid,
                payee_id,
                group_id,
                created_at,
                distribution,
                message,
            ) = res.fetchone()
            if rowid is None:
                return None

            payee = get_account_repository().fetch_one(id=payee_id)
            group = get_group_repository().fetch_one(group_id=group_id)
            tags = get_tag_repository().fetch_by_payment(payment_id=rowid)
            return Payment(
                id=rowid,
                payee=payee,
                group=group,
                created_at=datetime.datetime.strptime(created_at, "%d/%m/%Y"),
                distribution=distribution,
                message=message,
                tags=tags,
            )

    def fetch_all(self) -> [Payment]:
        with db.sqlite3_connection:
            account_repo = get_account_repository()
            pays: List[Payment] = []
            for (
                rowid,
                payee_id,
                group_id,
                created_at,
                distribution_json,
                message,
            ) in db.sqlite3_connection.execute(
                "SELECT rowid, payee_id, group_id, created_at, distribution, message FROM payments"
            ):
                payee = account_repo.fetch_one(id=payee_id)
                group = get_group_repository().fetch_one(group_id=group_id)
                tags = get_tag_repository().fetch_by_payment(payment_id=rowid)
                pays.append(
                    Payment(
                        id=rowid,
                        payee=payee,
                        group=group,
                        created_at=datetime.datetime.strptime(created_at, "%d/%m/%Y"),
                        distribution=json.loads(distribution_json),
                        message=message,
                        tags=tags,
                    )
                )

            return pays


def get_payment_repository() -> PaymentRepository:
    return _Sqlite3PaymentRepository()
