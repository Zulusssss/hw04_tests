from django.contrib.auth import get_user_model
from django.http import Http404
from django.test import TestCase, Client
from http import HTTPStatus

from django.urls import reverse

from ..models import Group, Post

User = get_user_model()



class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')  
        self.assertEqual(response.status_code, HTTPStatus.OK)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
    
    def setUp(self):
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)


    def test_public_urls_exists_at_desired_location(self):
        """Проверка доступности общедоступных страниц."""
        urls = {
            '/': HTTPStatus.OK,
            f'/group/{PostURLTests.group.slug}/': HTTPStatus.OK,
            f'/profile/{PostURLTests.user.username}/': HTTPStatus.OK,
            f'/posts/{PostURLTests.post.pk}/': HTTPStatus.OK,
        }
        for url, expected in urls.items():
            with self.subTest(url=url):
                self.assertEqual(
                    self.guest_client.get(url).status_code, expected)


    def test_authorized_urls_exists_at_desired_location(self):
        """Проверка доступности страниц для авторизированных пользователей."""
        urls = {
            f'/posts/{PostURLTests.post.pk}/edit/': HTTPStatus.OK,
            '/create/': HTTPStatus.OK,
        }
        for url, expected in urls.items():
            with self.subTest(url=url):
                self.assertEqual(
                    self.authorized_client.get(url).status_code, expected)
    

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': PostURLTests.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': PostURLTests.user.username}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': PostURLTests.post.pk}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': PostURLTests.post.pk}): 'posts/create_or_up_post.html',
            reverse('posts:post_create'): 'posts/create_or_up_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
    
    # def test_non_exist_url_404(self):
    #     with self.assertRaises(Http404):
    #         self.authorized_client.get('/bla-bla-bla/')

    def test_non_exist_url_404(self):
        self.assertEqual(self.guest_client.get('/bla-bla-bla/').status_code, HTTPStatus.NOT_FOUND)