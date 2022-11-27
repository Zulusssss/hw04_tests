from django.test import TestCase, Client
from http import HTTPStatus


class PostURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_public_urls_exists_at_desired_location(self):
        """Проверка доступности общедоступных страниц."""
        urls = {
            '/auth/signup/': HTTPStatus.OK,
            '/auth/logout/': HTTPStatus.OK,
            '/auth/login/': HTTPStatus.OK,
        }
        for url, expected in urls.items():
            with self.subTest(url=url):
                self.assertEqual(
                    self.guest_client.get(url).status_code, expected)
