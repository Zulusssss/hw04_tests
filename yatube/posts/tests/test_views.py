from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostTests(TestCase):
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
        self.authorized_client.force_login(PostTests.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug':
                    PostTests.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username':
                    PostTests.user.username}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id':
                    PostTests.post.pk}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id':
                    PostTests.post.pk}): 'posts/create_or_up_post.html',
            reverse('posts:post_create'): 'posts/create_or_up_post.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_show_correct_context(self):
        """Шаблон posr_edit сформирован с правильным контекстом."""
        url = reverse('posts:post_edit', kwargs={'post_id': PostTests.post.pk})
        response = self.authorized_client.get(url)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        url = reverse('posts:post_detail', kwargs={'post_id':
                      PostTests.post.pk})
        response = self.authorized_client.get(url)
        object = response.context['post']
        fields = {
            PostTests.post.text: object.text,
            PostTests.user.username: object.author.username,
        }

        for expected, value in fields.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.posts = []
        for i in range(0, 13):
            obj = Post.objects.create(
                author=cls.user,
                group=cls.group,
                text=f'Тестовый пост № {i}',
            )
            cls.posts.append(obj)

    def setUp(self):
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    def test_first_page_contains_ten_records(self):
        url_and_length = {
            reverse('posts:index'): 10,
            reverse('posts:group_list', kwargs={'slug':
                    PaginatorViewsTest.group.slug}): 10,
            reverse('posts:profile', kwargs={'username':
                    PaginatorViewsTest.user.username}): 2,
        }
        for url_rev, expected in url_and_length.items():
            with self.subTest(url_rev=url_rev):
                response = self.client.get(url_rev)
                value = len(response.context['page_obj'].object_list)
                self.assertEqual(value, expected)

    def test_last_page_contains_ten_records(self):
        url_and_length = {
            reverse('posts:index') + '?page=2': 3,
            reverse('posts:group_list', kwargs={'slug':
                    PaginatorViewsTest.group.slug}) + '?page=2': 3,
            reverse('posts:profile', kwargs={'username':
                    PaginatorViewsTest.user.username}) + '?page=7': 1,
        }
        for url_rev, expected in url_and_length.items():
            with self.subTest(url_rev=url_rev):
                response = self.client.get(url_rev)
                value = len(response.context['page_obj'].object_list)
                self.assertEqual(value, expected)

    def test_pages_contains_post_with_group(self):
        obj = Post.objects.create(
            author=PaginatorViewsTest.user,
            group=PaginatorViewsTest.group,
            text='Тестовый пост № АААААА',
        )

        url_and_obj = {
            reverse('posts:index'): obj,
            reverse('posts:group_list', kwargs={'slug':
                    PaginatorViewsTest.group.slug}): obj,
            reverse('posts:profile', kwargs={'username':
                    PaginatorViewsTest.user.username}): obj,
        }

        for url_rev, val in url_and_obj.items():
            with self.subTest(url_rev=url_rev):
                response = self.client.get(url_rev)
                page_obj = response.context['page_obj']
                list_of_objects_on_page = page_obj.object_list
                self.assertIn(val, list_of_objects_on_page)
