from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse
from ..forms import PostForm
from ..models import Group, Post
from ..utils import paginator
from ..views import NUMBER_OF_POSTS, PAGE_POSTS_OF_USER

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
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        url = reverse('posts:post_edit', kwargs={'post_id': PostTests.post.pk})
        response = self.authorized_client.get(url)
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertEqual(response.context['is_edit'], True)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        url = reverse('posts:post_detail', kwargs={'post_id':
                      PostTests.post.pk})
        response = self.authorized_client.get(url)
        object = response.context['post']
        self.assertEqual(object, PostTests.post)


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
        '''
        На первой странице каталога находится планируемое число записей.
        '''
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
        '''
        На последней странице каталога находится планируемое число записей.
        '''
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
        '''На страницах отображается новый созданный пост.'''
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

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        url = reverse('posts:index')
        response = self.authorized_client.get(url)
        object = response.context['page_obj']
        post_list = Post.objects.select_related('author', 'group').all()
        page_obj = paginator(response.context['request'],
                             post_list, NUMBER_OF_POSTS)
        self.assertEqual(object.object_list, list(page_obj.object_list))
        self.assertIsInstance(object, type(page_obj))

    def test_group_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        url = reverse('posts:group_list', kwargs={'slug':
                      PaginatorViewsTest.group.slug})
        response = self.authorized_client.get(url)
        object = response.context['page_obj']
        group = Group.objects.get(slug=PaginatorViewsTest.group.slug)
        post_list = group.posts.all()
        page_obj = paginator(response.context['request'],
                             post_list, NUMBER_OF_POSTS)
        self.assertEqual(object.object_list, list(page_obj.object_list))
        self.assertIsInstance(object, type(page_obj))

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        url = reverse('posts:profile', kwargs={'username':
                      PaginatorViewsTest.user.username})
        response = self.authorized_client.get(url)
        object = response.context['page_obj']
        user = User.objects.get(username=PaginatorViewsTest.user.username)
        post_list = user.posts.all()
        page_obj = paginator(response.context['request'],
                             post_list, PAGE_POSTS_OF_USER)
        self.assertEqual(object.object_list, list(page_obj.object_list))
        self.assertIsInstance(object, type(page_obj))
