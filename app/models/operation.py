from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Operation(models.Model):
    OPERATION_TYPES = [
        ('replenishment', 'Пополнение'),
        ('transfer', 'Перевод'),
    ]

    sender = models.ForeignKey(User, verbose_name='Отправитель', on_delete=models.CASCADE, 
                               related_name='sender_operations')
    receiver = models.ForeignKey(User, verbose_name='Получатель', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='receiver_operations')
    type = models.CharField(max_length=20, choices=OPERATION_TYPES)
    amount = models.DecimalField(verbose_name='Сумма', decimal_places=2, max_digits=20, default=0,
                                 validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now_add=True)
    resulting_balance = models.DecimalField(verbose_name='Баланс после операции', decimal_places=2, max_digits=20,
                                            null=True, blank=True)

    def __str__(self):
        return f'{self.sender.username} {self.type} {self.amount}'
