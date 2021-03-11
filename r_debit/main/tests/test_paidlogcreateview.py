from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from main import factories
from main import models

class TestPaidLogCreateView(TestCase):
    
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_working(self):
        debit = factories.DebitFactory(user = self.user)
        customer = factories.CustomerFactory(debit = debit)
        url = reverse('main:paidlog-create', kwargs = {'debit_pk': debit.pk})
        data = {
            'amount': 120,
            'customer_name': customer.name
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('main:paidlog-list', kwargs = {'customer_pk': customer.pk}))
        self.assertEqual(len(models.PaidLog.objects.all()), 1)

        # test message
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, 'success')
        self.assertEqual(all_messages[0].message, '{} paid {}. Added successfully'.format(customer.name, data['amount']))
    
    def test_with_non_existing_customer(self):
        debit = factories.DebitFactory(user = self.user)
        url = reverse('main:paidlog-create', kwargs = {'debit_pk': debit.pk})
        data = {
            'amount': 120,
            'customer_name': 'shibu tp'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('main:customer-log', kwargs = {'debit_pk': debit.pk}))
        self.assertEqual(len(models.PaidLog.objects.all()), 0)

        # error message
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, 'error')
        self.assertEqual(all_messages[0].message, 'Customer name not found!')
    
    def test_permission(self):
        debit = factories.DebitFactory()
        customer = factories.CustomerFactory(debit = debit)
        url = reverse('main:paidlog-create', kwargs = {'debit_pk': debit.pk})
        data = {
            'amount': 120,
            'customer_name': customer.name
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
