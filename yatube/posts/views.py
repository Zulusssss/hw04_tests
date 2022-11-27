from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import paginator
from django.contrib.auth.decorators import login_required

NUMBER_OF_POSTS = 10
PAGE_POSTS_OF_USER = 2


def index(request):
    '''
    Позволяет перенести в HTML-код главной страницы сайта записи из
    таблицы "Post" из БД для тега <main> и строку для тега <title>.
    Записи из "Post" отсортированы по убыванию даты публикации.
    Записей взято - первые 10 штук.
    '''
    post_list = Post.objects.select_related('author', 'group').all()
    page_obj = paginator(request, post_list, NUMBER_OF_POSTS)
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    '''
    Позволяет перенести в HTML-код страницы данной группы постов записи из
    таблицы "Post" из БД для тега <main> и строку для тега <title>.
    Записи из "Post" отсортированы по убыванию даты публикации и соответствуют
    определённой группе, которая оп-ся, исходя из значения "slug".
    Записей взято - первые 10 штук.
    '''
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = paginator(request, posts, NUMBER_OF_POSTS)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    '''
    Переводит на страницу с постами конкретного пользователя.
    '''
    user = User.objects.get(username=username)
    post_list = user.posts.all()
    number_post_of_user = post_list.count()
    page_obj = paginator(request, post_list, PAGE_POSTS_OF_USER)
    templates = 'posts/profile.html'
    context = {
        'number_post_of_user': number_post_of_user,
        'username': user,
        'page_obj': page_obj,
    }
    return render(request, templates, context)


def post_detail(request, post_id):
    '''
    Переводит на страницу с информацией конкретного поста.
    Если вы являетесь автором данного поста, то вам будет
    доступна кнопка "редактировать запись".
    '''
    post = Post.objects.get(pk=post_id)
    number_post_of_user = Post.objects.filter(author=post.author).count()

    templates = 'posts/post_detail.html'
    context = {
        'number_post_of_user': number_post_of_user,
        'post': post,
    }
    return render(request, templates, context)


@login_required
def post_create(request):
    '''
    Переводит на страницу с формой для создания нового поста.
    '''
    groups = Group.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)

        return render(request, 'posts/create_or_up_post.html',
                      {'form': form, 'groups': groups, })

    form = PostForm()
    return render(request, 'posts/create_or_up_post.html',
                  {'form': form, 'groups': groups, })


@login_required
def post_edit(request, post_id):
    '''
    Переводит на страницу редактирования поста.
    '''
    is_edit = True
    post = Post.objects.get(pk=post_id)
    id_author = post.author
    groups = Group.objects.all()
    if id_author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)

            if form.is_valid():
                form.save()
                return redirect('posts:post_detail', post_id)

            return render(request, 'posts/create_or_up_post.html',
                          {'form': form, 'post': post,
                           'is_edit': is_edit, 'groups': groups, })

        form = PostForm()
        return render(request, 'posts/create_or_up_post.html',
                      {'form': form, 'post': post,
                       'is_edit': is_edit, 'groups': groups, })

    return redirect('posts:post_detail', post_id)
