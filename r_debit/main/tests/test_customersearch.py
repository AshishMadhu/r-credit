from django.http import response
from django.test import TestCase
from django.urls import reverse

from main import factories

class TestCustomerTestView(TestCase):
    
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_working(self):
        debit = factories.DebitFactory(user = self.user)
        factories.CustomerFactory(debit = debit, name = 'kannan')
        factories.CustomerFactory(debit = debit, name = 'kubaran')
        factories.CustomerFactory(debit = debit, name = 'adhi')
        url = reverse('main:api:search-customer', kwargs = {'debit_pk': debit.pk}) + '?name=a'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'adhi')
        
        url = reverse('main:api:search-customer', kwargs = {'debit_pk': debit.pk}) + '?name=k'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'kannan')
    
    def test_with_other_debit(self):
        debit = factories.DebitFactory()
        url = reverse('main:api:search-customer', kwargs = {'debit_pk': debit.pk}) + '?name=a'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)