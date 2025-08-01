import pytest
from decimal import Decimal
from app.services.replenishment import replenishment
from app.services.transfer import transfer


@pytest.mark.django_db
class TestAccountOperations:
    # === ПОПОЛНЕНИЕ ===
    def test_replenishment_success(self, user1):
        old_balance = user1.user_account.balance
        op = replenishment(user1.id, Decimal('2500'))

        user1.user_account.refresh_from_db()
        assert user1.user_account.balance == old_balance + Decimal('25.00')
        assert op.type == 'replenishment'
        assert op.amount == Decimal('25.00')
        assert op.resulting_balance == user1.user_account.balance
        assert op.sender == user1
        assert op.receiver == user1


    def test_replenishment_zero(self, user1):
        with pytest.raises(ValueError, match='Сумма пополнения должна быть больше 0'):
            replenishment(user1.id, Decimal('0'))


    def test_replenishment_negative(self, user1):
        with pytest.raises(ValueError, match='Сумма пополнения должна быть больше 0'):
            replenishment(user1.id, Decimal('-10.00'))


    # === ПЕРЕВОД ===
    def test_transfer_success(self, user1, user2):
        from app.services.replenishment import replenishment

        # Пополняем счёт user1
        replenishment(user1.id, Decimal('10000'))

        # Обновляем объекты из базы
        user1.user_account.refresh_from_db()
        user2.user_account.refresh_from_db()

        # Сохраняем баланс после пополнения
        sender_balance = user1.user_account.balance
        receiver_balance = user2.user_account.balance

        # Перевод
        op = transfer(user1.id, user2.id, Decimal('30.00'))

        # Обновляем снова после перевода
        user1.user_account.refresh_from_db()
        user2.user_account.refresh_from_db()

        # Проверяем
        assert user1.user_account.balance == sender_balance - Decimal('30.00')
        assert user2.user_account.balance == receiver_balance + Decimal('30.00')
        assert op.type == 'transfer'
        assert op.amount == Decimal('30.00')
        assert op.resulting_balance == user1.user_account.balance
        assert op.sender == user1
        assert op.receiver == user2


    def test_transfer_to_self(self, user1):
        with pytest.raises(ValueError, match='Нельзя перевести самому себе'):
            transfer(user1.id, user1.id, Decimal('10.00'))


    def test_transfer_insufficient_funds(self, user1, user2):
        with pytest.raises(ValueError, match='Недостаточно средств'):
            transfer(user1.id, user2.id, Decimal('1000.00'))


    def test_transfer_zero(self, user1, user2):
        with pytest.raises(ValueError, match='Сумма перевода должна быть больше 0'):
            transfer(user1.id, user2.id, Decimal('0'))


    def test_transfer_negative(self, user1, user2):
        with pytest.raises(ValueError, match='Сумма перевода должна быть больше 0'):
            transfer(user1.id, user2.id, Decimal('-5.00'))
