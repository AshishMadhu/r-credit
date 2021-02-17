from uuid import uuid4
from django.http import response
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from main import factories

class TestPaidLogViewSet(APITestCase):
    
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def create_models(self):
        debit = factories.DebitFactory(user = self.user)
        customer = factories.CustomerFactory(debit = debit)
        paidlog = factories.PaidLogFactory(customer = customer)
        return [debit, customer, paidlog]

    def test_detail_view(self):
        [debit, customer, paidlog] = self.create_models()
        url = reverse('main:api:paidlog-detail', kwargs = {'customer_pk': customer.pk, 'pk': paidlog.pk})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], paidlog.amount)
    
    def test_list_view(self):
        [debit, customer, paidlog] = self.create_models()
        factories.PaidLogFactory(customer = customer)
        factories.PaidLogFactory()
        url = reverse('main:api:paidlog-list', kwargs = {'customer_pk': customer.pk})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_create_view(self):
        # api is called with customer_pk so this id is used to create model
        [debit, customer, paidlog] = self.create_models()
        data = {
            'amount': 200
        }
        url = reverse('main:api:paidlog-list', kwargs = {'customer_pk': customer.pk})
        response = self.client.post(url, data = data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], 200)
    
    def test_create_view_with_others_customers(self):
        customer = factories.CustomerFactory()
        url = reverse('main:api:paidlog-list', kwargs = {'customer_pk': customer.pk})
        response = self.client.post(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_view_with_non_existing_customer(self):
        id = uuid4()
        url = reverse('main:api:paidlog-list', kwargs = {'customer_pk': id})
        response = self.client.post(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_view(self):
        [debit, customer, paidlog] = self.create_models()
        data = {
            'amount': 220
        }
        url = reverse('main:api:paidlog-detail', kwargs = {'customer_pk': customer.pk, 'pk': paidlog.pk})
        response = self.client.patch(url, data = data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], 220)

    def test_delete_view(self):
        [debit, customer, paidlog] = self.create_models()
        url = reverse('main:api:paidlog-detail', kwargs = {'customer_pk': customer.pk, 'pk': paidlog.pk})
        response = self.client.delete(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permission(self):
        debit = factories.DebitFactory()
        customer = factories.CustomerFactory(debit = debit)
        paidlog = factories.PaidLogFactory(customer = customer)
        url = reverse('main:api:paidlog-detail', kwargs = {'customer_pk': customer.pk, 'pk': paidlog.pk})
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
