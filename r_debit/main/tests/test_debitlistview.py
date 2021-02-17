from django.urls import reverse
from django.test import TestCase
from rest_framework import status

from main import factories

class TestDebitListView(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    def test_working(self):
        factories.DebitFactory()
        for i in range(5):
            factories.DebitFactory(user = self.user)
        url = reverse('main:debit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['object_list']), 5)

