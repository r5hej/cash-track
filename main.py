from persistence.account import get_account_repository
from persistence.group import get_group_repository
from persistence.payment import get_payment_repository
from http_api.server import init_server

def main():
    init_server()
    # user_test()
    # group_test()
    # payment_test()


def payment_test():
    payment_repo = get_payment_repository()
    group_repo = get_group_repository()
    account_repo = get_account_repository()

    group = group_repo.fetch_all()[0]
    account = account_repo.fetch_all()[0]
    payment = payment_repo.create(payee=account, group=group, distribution={account.id: 100}, message='first payment')
    print(payment)

    for p in payment_repo.fetch_all():
        print(p)

    

def group_test():
    repo = get_group_repository()
    repo.create(name='fiske gruppen')
    for g in repo.fetch_all():
        print(g)



def user_test():
    user_repo = get_account_repository()
    user_repo.create(name='pusling', username='super pus')

    users = user_repo.fetch_all()
    for user in users:
        print(user)


if __name__ == '__main__':
    main()
