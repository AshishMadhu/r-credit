from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main import factories

class TestDebitLogUpdateView(APITestCase):
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_working(self):
        debit = factories.DebitFactory(user = self.user)
        customer = factories.CustomerFactory(debit = debit)
        debitlog = factories.DebitLogFactory(customer = customer)
        data = {
            'paid': True,
        }
        url = reverse('main:api:debitlog-update', kwargs = {'debitlog_pk': debitlog.pk})
        response = self.client.patch(url, data = data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['paid'], True)

