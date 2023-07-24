from django.template import Template, Context

import pytest
from auctions.tests.factories import CategoryFactory


pytestmark = pytest.mark.django_db


class TestCategoryTag:
    def test_five_categories_render(self):
        categories = [CategoryFactory() for _ in range(5)]
        template = Template("{% load category_tag %}{% show_categories %}<h1>Hello</h1>")
        rendered =template.render(Context({}))
        
        for category in categories:
            assert category.title in rendered
            assert category.get_absolute_url() in rendered
    
    def test_zero_categories_render(self):
        categories = None
        template = Template("{% load category_tag %}{% show_categories %}<h1>Hello</h1>")
        rendered =template.render(Context({'categories': categories}))
        
        assert 'There are no categories.' in rendered