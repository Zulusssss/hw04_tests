from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse

User = get_user_model()

class PostFormTests(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.user = User.objects.create_user(username='auth')
    
    def setUp(self):
        self.guest_client = Client()
    
    def test_create_user(self):
        users_count = User.objects.count()
        form_data = {
            'first_name': 'Первое имя',
            'last_name': 'Последнее имя',
            'username': 'auth',
            'email': 'auth@gmai.com',
            'password1': 'Epick_sword123',
            'password2': 'Epick_sword123',

        }
        response = self.guest_client.post(
            reverse('users:signup'), 
            data=form_data,
            follow=True
        )
        url = reverse('posts:index')
        self.assertRedirects(response, url)
        self.assertEqual(User.objects.count(), users_count+1)
        
        self.assertTrue(
            User.objects.filter(
                first_name='Первое имя',
                last_name='Последнее имя',
                username='auth',
                email='auth@gmai.com',
                ).exists()
        )
