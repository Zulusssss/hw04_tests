from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    '''
    Класс формы для создания формы создания/редактирования записи.
    Связан с моделью Post.
    '''
    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': ('Текст поста'),
            'group': ('Необязательная группа, к которой можно отнести пост'),
        }
