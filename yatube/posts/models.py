from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    '''
    Модель для создания таблицы "Group".
    Таблица используется для хранения групп, в которые
    объединяются выкладываемые посты.
    Поля таблицы: "title", "slug", "description".
    '''
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title


class Post(models.Model):
    '''
    Модель для создания таблицы "Post".
    В данной таблице хранятся тексты, их авторы и даты публикации.
    Поля таблицы: "text", "pub_date", "author".
    '''
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор"
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name="Группа"
    )

    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        NUMBER_OF_CHAR = 15
        return self.text[:NUMBER_OF_CHAR]
