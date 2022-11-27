from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    '''
    Класс для статичного шаблона с информацией о создателе сайта.
    '''
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    '''
    Класс для статичного шаблона с информацией о технологиях,
    которыми владеет создатель сайта.
    '''
    template_name = 'about/tech.html'
