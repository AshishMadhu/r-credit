from django.test import TestCase
from django.urls import reverse

from main import factories

class TestDebitlogDeleteView(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_deletion(self):
        debit = factories.DebitFactory(user = self.user)
        customer = factories.CustomerFactory(debit = debit)
        debitlog = factories.DebitLogFactory(customer = customer)
        url = reverse('main:debitlog-delete', kwargs = {'debitlog_pk': debitlog.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        # decode 'cause content is a b str
        self.assertEqual(response.content.decode('utf-8'), 'success')
    
    def test_signal(self):
        debit = factories.DebitFactory(user = self.user)
        customer = factories.CustomerFactory(debit = debit)
        debitlog = factories.DebitLogFactory(customer = customer, amount = 100)
        factories.DebitLogFactory(customer = customer, amount = 100)
        self.assertEqual(customer.total, 200)
        url = reverse('main:debitlog-delete', kwargs = {'debitlog_pk': debitlog.pk})
        response = self.client.post(url)
        customer.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(customer.total, 100)


