from decimal import Decimal

from django.db import transaction

from app.models import Account, Operation


@transaction.atomic
def transfer(sender_id: int, receiver_id: int, amount: Decimal) -> Operation:
    if amount <= 0:
        raise ValueError('Сумма перевода должна быть больше 0')

    if sender_id == receiver_id:
        raise ValueError('Нельзя перевести самому себе')

    sender = Account.objects.select_for_update().get(user_id=sender_id)
    receiver = Account.objects.select_for_update().get(user_id=receiver_id)

    if sender.balance < int(amount):
        raise ValueError('Недостаточно средств')

    sender.balance -= int(amount)
    receiver.balance += int(amount)

    sender.save()
    receiver.save()

    return Operation.objects.create(
        sender_id=sender_id,
        type='transfer',
        amount=int(amount),
        receiver_id=receiver_id,
        resulting_balance = sender.balance
    )
