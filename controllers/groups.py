from typing import Optional, List
from persistence.group import get_group_repository
from persistence.account import get_account_repository
from domain_model.group import Group


def get_groups(group_id: Optional[int]) -> List[Group]:
    repo = get_group_repository()
    if group_id is None:
        return repo.fetch_all()

    group = repo.fetch_one(group_id=group_id)
    if group is None:
        return []
    
    return [group]
    


def create_group(name: str) -> None:
    repo = get_group_repository()
    group = repo.create(name=name, accounts=[])
    print(f"Created group {group}")
    


def delete_group(group_id: int) -> None:
    repo = get_group_repository()
    group = repo.fetch_one(group_id=group_id)
    if group is None:
        raise Exception('group not found')
    
    repo.delete(group=group)


def add_account_to_group(group_id: int, account_id: int) -> None:
    account_repo = get_account_repository()
    account = account_repo.fetch_one(id=account_id)
    if account is None:
        raise Exception(f'Could not find account with id {account_id}')

    group_repo = get_group_repository()
    group = group_repo.fetch_one(group_id=group_id)
    if group_id is None:
        raise Exception(f'Could not find group with id {group_id}')
    
    group_repo.add_account(account=account, group=group)



def remove_account_to_group(group_id: int, account_id: int) -> None:
    account_repo = get_account_repository()
    account = account_repo.fetch_one(id=account_id)
    if account is None:
        raise Exception(f'Could not find account with id {account_id}')

    group_repo = get_group_repository()
    group = group_repo.fetch_one(group_id=group_id)
    if group_id is None:
        raise Exception(f'Could not find group with id {group_id}')
    
    group_repo.remove_account(account=account, group=group)