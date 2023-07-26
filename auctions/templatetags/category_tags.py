from django import template
from auctions.models import Category

register = template.Library()

@register.inclusion_tag('includes/_categories.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('includes/_categories_card.html')
def categories_card():
    categories = Category.objects.all()
    return {'categories': categories}