from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main import factories

class TestSearchCustomer(APITestCase):
    
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_working(self):
        debit = factories.DebitFactory(user = self.user)
        customer = factories.CustomerFactory(debit = debit, name = "kannan")
        customer2 = factories.CustomerFactory(debit = debit, name = 'kabir')
        factories.DebitLogFactory(customer = customer)
        factories.DebitLogFactory(customer = customer2)
        url = reverse('main:api:search-customer', kwargs = {'debit_pk': debit.id}) + '?name=kannan'
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_without_name(self):
        debit =  factories.DebitFactory(user = self.user)
        customer = factories.CustomerFactory(debit = debit, name = 'kannan')
        factories.DebitLogFactory(customer = customer)
        url = reverse('main:api:search-customer', kwargs = {'debit_pk': debit.pk}) + '?name='
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'You need to pass name as params!')
    
    def test_permission(self):
        anonymous_debit = factories.DebitFactory()
        url = reverse('main:api:search-customer', kwargs = {'debit_pk': anonymous_debit.pk}) + '?name=kannan'
        response = self.client.get(url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
