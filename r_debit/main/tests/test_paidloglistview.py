from django.test import TestCase
from django.urls import reverse
from main import factories

class TestPaidLogListView(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(username = 'atom', password = 'TestPass@123')
        self.client.force_login(self.user)
    
    