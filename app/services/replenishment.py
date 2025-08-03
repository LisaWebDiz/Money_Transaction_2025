from decimal import Decimal

from django.db import transaction

from app.models import Account, Operation


@transaction.atomic
def replenishment(user_id: int, amount: Decimal) -> Operation:
    if amount <= Decimal('0'):
        raise ValueError('Сумма пополнения должна быть больше 0')

    # amount в копейках → переводим в рубли
    amount_rub = amount / 100

    account = Account.objects.select_for_update().get(user_id=user_id)
    account.balance += amount_rub
    account.save()

    return Operation.objects.create(
        sender_id=user_id,
        receiver_id=user_id,
        type=Operation.REPLENISHMENT,
        amount=amount_rub,  # сохраняем в рублях
        resulting_balance=account.balance
    )
