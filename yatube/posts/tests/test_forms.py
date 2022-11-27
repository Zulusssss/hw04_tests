from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from django.urls import reverse

from ..models import Group, Post

User = get_user_model()

class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
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
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)
    
    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовое описание №1',
            'group': PostFormTests.group.pk,
            'author': PostFormTests.user,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'), 
            data=form_data,
            follow=True
        )
        url = reverse('posts:profile', kwargs={'username': response.context['request'].user.username})
        self.assertRedirects(response, url)
        self.assertEqual(Post.objects.count(), posts_count+1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовое описание №1',
                group=PostFormTests.group.pk,
                author=PostFormTests.user
                ).exists()
        )


    def test_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовое описание №1',
            'group': PostFormTests.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': PostFormTests.post.pk}), 
            data=form_data,
            follow=True
        )
        # 
        url = reverse('posts:post_detail', kwargs={'post_id': PostFormTests.post.pk})
        self.assertRedirects(response, url)
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовое описание №1',
                group=PostFormTests.group.pk,
                author=PostFormTests.user
                ).exists()
        )








































