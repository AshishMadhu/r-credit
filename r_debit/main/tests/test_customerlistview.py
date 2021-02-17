from uuid import uuid4
from django import test
from django.http import response
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from main import factories
from main import models

class TestCustomerListView(test.TestCase):
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_with_debit_not_existing(self):
        uuid = uuid4()
        response = self.client.get(reverse('main:customer-log', kwargs = {'debit_pk': uuid}))
        self.assertEqual(response.status_code, 404)
    
    def test_context_obj(self):
        debit = factories.DebitFactory(user = self.user, name = 'shop')
        response = self.client.get(reverse('main:customer-log', kwargs = {'debit_pk': debit.pk}))
        self.assertIn('debit_id', response.context)

    def test_view_queryset(self):
        debit = factories.DebitFactory(user = self.user)
        debit2 = factories.DebitFactory()
        for i in range(10):
            customer = factories.CustomerFactory(debit = debit)
            factories.DebitLogFactory(customer = customer)
        for i in range(3):
            customer = factories.CustomerFactory(debit = debit2)
            factories.DebitLogFactory(customer = customer)
        url = reverse('main:customer-log', kwargs = {'debit_pk': debit.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 6) # 6 'cause pagination
    
    def test_permissions(self):
        # other users debit cannot be accessed
        debit = factories.DebitFactory()
        url = reverse('main:customer-log', kwargs = {'debit_pk': debit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_with_other_user_debit(self):
        user = factories.UserFactory(username = 'kannan', password = 'TestPass@123')
        debit = factories.DebitFactory(user = user, name = 'shop')
        response = self.client.get(reverse('main:customer-log', kwargs = {'debit_pk': debit.id}))
        self.assertEqual(response.status_code, 403)
    
    def test_sorting(self):
        debit = factories.DebitFactory(user = self.user)
        for i in range(5):
            customer = factories.CustomerFactory(debit = debit)
            factories.DebitLogFactory(customer = customer)
        url = reverse('main:customer-log', kwargs = {'debit_pk': debit.id}) + '?sort=customer_number'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)