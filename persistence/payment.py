from domain_model.payment import PaymentRepository, Payment
from domain_model.account import Account
from domain_model.group import Group
from typing import Optional, Dict, List
import persistence.db as db
import json
from persistence.account import get_account_repository

class _Sqlite3PaymentRepository(PaymentRepository):
    """"""
    def __init__(self) -> None:
        super().__init__()
        db._init_db_if_not_yet()

    def create(
        self,
        payee: Account,
        group: Group,
        distribution: Dict[Account, int] = {},
        message: Optional[str] = None,
    ) -> Payment:
        data = {
            'payee_id': payee.id,
            'group_id': group.id,
            'distribution': json.dumps(distribution)
        }
        if message is not None:
            data['message'] = message

        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute('INSERT INTO payments VALUES (:payee_id, :group_id, :distribution, :message)', data)
            return Payment(id=res.lastrowid, payee=Account, createdAt=None, distribution=distribution, message=message)

    def update_distribution(self, payment: Payment, distribution: Dict[Account, int]) -> None:
        raise Exception('Not implemented')
    

    def delete(self, payment: Payment) -> None:
        with db.sqlite3_connection:
            db.sqlite3_connection.execute('DELETE FROM payments where rowid = ?', (payment.id,))


    def fetch_one(self, id: int) -> Optional[Payment]:
        with db.sqlite3_connection:
            res = db.sqlite3_connection.execute('SELECT rowid, payee_id, group_id, distribution, message FROM payments WHERE rowid = ?', (Payment.id,))
            rowid, payee_id, group_id, distribution, message = res.fetchone()
            if rowid is None:
                return None
            
            payee = get_account_repository().fetch_one(id=payee_id)
            return Payment(id=rowid, payee=payee, createdAt=None, distribution=distribution, message=message)
            
    
    def fetch_all(self) -> [Payment]:
        with db.sqlite3_connection:
            account_repo = get_account_repository()
            pays: List[Payment] = []
            for id, payee_id, group_id, distribution_json, message in db.sqlite3_connection.execute('SELECT rowid, payee_id, group_id, distribution, message FROM payments'):
                payee = account_repo.fetch_one(id=payee_id)

                pays.append(Payment(id=id, payee=payee, createdAt=None, distribution=json.loads(distribution_json), message=message))
                
            return pays

def get_payment_repository() -> PaymentRepository:
    return _Sqlite3PaymentRepository()




