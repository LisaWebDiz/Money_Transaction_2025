from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, verbose_name='Держатель счета', on_delete=models.CASCADE,
                                related_name='user_account')
    balance = models.DecimalField(verbose_name='Баланс счета', decimal_places=2, max_digits=20, default=0,
                                  validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f'{self.user.username}: {self.balance} руб.'
