from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post, NUMBER_OF_CHAR

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        act = group.__str__()
        expected = group.title
        self.assertEqual(act, expected, '__str__ не выводит self.title')

        post = PostModelTest.post
        act = post.__str__()
        expected = post.text[:NUMBER_OF_CHAR]
        self.assertEqual(act, expected,
                         '__str__ не выводит self.text[:NUMBER_OF_CHAR]')

    def test_models_have_correct_varbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата',
            'author': 'Автор',
            'group': 'Группа',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(post._meta.get_field(value).verbose_name,
                                 expected,)
