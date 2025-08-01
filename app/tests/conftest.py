import pytest

@pytest.fixture
def user1(db):
    from django.contrib.auth.models import User
    from app.models import Account

    user = User.objects.create_user(username='user1', password='1111')
    Account.objects.get_or_create(user=user)
    return user

@pytest.fixture
def user2(db):
    from django.contrib.auth.models import User
    from app.models import Account

    user = User.objects.create_user(username='user2', password='2222')
    Account.objects.get_or_create(user=user)
    return user
