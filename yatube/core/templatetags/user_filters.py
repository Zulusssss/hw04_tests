from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    '''
    Ф-ия для добавления класса css в HTML-шаблонах.
    '''
    return field.as_widget(attrs={'class': css})
