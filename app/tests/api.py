import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
class TestAccountAPI:
    def setup_method(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

    def test_my_account(self):
        url = reverse('account-my-account')
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'balance' in response.data

    def test_my_operations_empty(self):
        url = reverse('operation-my-operations')
        response = self.client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) == 0

    def test_replenish_success(self):
        url = reverse('operation-replenish')
        data = {'amount': '50.00'}
        response = self.client.post(url, data)
        assert response.status_code == 200
        assert response.data['amount'] == '0.50'
        assert response.data['type'] == 'replenishment'

    def test_replenish_invalid_amount(self):
        url = reverse('operation-replenish')
        data = {'amount': '0'}
        response = self.client.post(url, data)
        assert response.status_code == 400

    def test_transfer_success(self):
        replenish_url = reverse('operation-replenish')
        self.client.post(replenish_url, {'amount': '10000'})

        url = reverse('operation-transfer')
        data = {
            'receiver_id': self.user2.id,
            'amount': '30.00'
        }
        response = self.client.post(url, data)
        assert response.status_code == 200
        assert response.data['amount'] == '30.00'
        assert response.data['type'] == 'transfer'
        assert response.data['sender'] == self.user1.id
        assert response.data['receiver'] == self.user2.id

    def test_transfer_to_self(self):
        url = reverse('operation-transfer')
        data = {
            'receiver_id': self.user1.id,
            'amount': '10.00'
        }
        response = self.client.post(url, data)
        assert response.status_code == 400
        assert 'error' in response.data

    def test_transfer_insufficient_funds(self):
        url = reverse('operation-transfer')
        data = {
            'receiver_id': self.user2.id,
            'amount': '1000.00'
        }
        response = self.client.post(url, data)
        assert response.status_code == 400
        assert 'error' in response.data
