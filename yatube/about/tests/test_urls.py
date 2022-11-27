from django.test import TestCase, Client
from http import HTTPStatus


class AboutURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_public_urls_exists_at_desired_location(self):
        """Проверка доступности общедоступных страниц."""
        urls = {
            '/about/author/': HTTPStatus.OK,
            '/about/tech/': HTTPStatus.OK,
        }

        for url, expected in urls.items():
            with self.subTest(url=url):
                self.assertEqual(
                    self.guest_client.get(url).status_code, expected)

    def test_non_exist_url_404(self):
        self.assertEqual(self.guest_client.get('/bla-bla-bla/').status_code,
                         HTTPStatus.NOT_FOUND)
