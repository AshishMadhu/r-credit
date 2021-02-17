from django.urls import reverse
from rest_framework.test import APITestCase
from knox.models import AuthToken

class TestRegisterView(APITestCase):
    def test_working(self):
        url = reverse('accounts:api:register')
        data = {
            'username': 'atom',
            'password': 'TestPassword@123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(AuthToken.objects.all()), 1)
        self.assertEqual(response.data['user']['username'], 'atom')