from django.core.paginator import Paginator


def paginator(request, queryset, number_of_notes):
    '''
    Ф-ия использует Paginator из Django для разбиения информации на страницы.
    Здесь мы разбиваем кверисет записей из таблицы из БД на страницы, на каждой
    из которых определённое число записей. А затем возвращаем одну из страниц.
    Входные аргументы:
    request - запрос
    queryset - множество записей из таблицы из БД
    number_of_notes - число записей из таблицы из БД на одной странице
    Выходные аргументы:
    Одна страница (из кучи страниц) с определённым числом записей на ней.
    '''
    paginator = Paginator(queryset, number_of_notes)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
