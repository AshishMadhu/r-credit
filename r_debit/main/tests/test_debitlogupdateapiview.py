from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from main import factories

class TestDebitLogUpdateAPIView(APITestCase):

    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_working(self):
        debit = factories.DebitFactory(user = self.user)
        customer = factories.CustomerFactory(debit = debit)
        customer1 = factories.CustomerFactory(debit = debit)
        debitlog = factories.DebitLogFactory(customer = customer)
        url = reverse('main:api:debitlog-update', kwargs = {'debitlog_pk': debitlog.pk})

        # ? testing put
        data = {
            'customer_name': customer1.name,
            'amount': 200,
            'paid': True
        }
        response = self.client.put(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], data['amount'])
        self.assertEqual(response.data['customer_name'], data['customer_name'])

        # ? testing patch
        data = {
            'customer_name': customer.name,
            'paid': False,
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], data['customer_name'])
        self.assertEqual(response.data['paid'], data['paid'])

    def test_to_add_customer_from_others_debit_to_this_debitlog(self):
        # this is also a test for non-existing customer_name is passed as data same output
        customer = factories.CustomerFactory()

        debit2 = factories.DebitFactory(user = self.user)
        customer2 = factories.CustomerFactory(debit = debit2)
        debitlog2 = factories.DebitLogFactory(customer = customer2)

        url = reverse('main:api:debitlog-update', kwargs = {'debitlog_pk': debitlog2.pk})
        data = {
            'customer_name': customer.name,
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['customer_name'], 'There is no customer with this name!')


