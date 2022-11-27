from .forms import CreationForm

from django.views.generic import CreateView

from django.urls import reverse_lazy


class SignUp(CreateView):
    '''
    Класс представления(CBV) для формирования страницы
    регистрации пользователей.
    '''
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('posts:index')
