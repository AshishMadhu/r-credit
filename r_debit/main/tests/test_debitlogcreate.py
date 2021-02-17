from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls.base import reverse
from main import models
from main import factories


class TestDebitlogCreateView(TestCase):

    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_debitlog_create(self):
        data = {
            'customer_name': 'Kannan',
            'amount': '10',
        }
        debit = factories.DebitFactory(user = self.user, name = 'shop')
        url = reverse('main:debitlog-create', kwargs = {'debit_pk': debit.id})
        response = self.client.post(url, data)
        # this will redirect if everything runs well
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(models.DebitLog.objects.all()), 1)

        # test same name with customer_name kAnnAn
        data['customer_name'] = 'kAnnAn'
        with self.assertLogs('main.views', level = 'INFO') as cm: # just check log is called
            response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        print(models.DebitLog.objects.all())
        self.assertEqual(len(models.DebitLog.objects.all()), 2)
        self.assertEqual(len(models.Customer.objects.all()), 1)
        self.assertEqual(models.Customer.objects.first().name, 'Kannan')

    def test_permission(self):
        # other loggedin user cannot create debitlog on others debit
        debit = factories.DebitFactory()
        url = reverse('main:debitlog-create', kwargs = {'debit_pk': debit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    def test_with_deleted_debitlog_id(self):
        # ! Unfinished
        uuid = str(uuid4())
        response = self.client.get(reverse('main:customer-log', kwargs = {'debit_pk': uuid}))
        self.assertEqual(response.status_code, 404)
