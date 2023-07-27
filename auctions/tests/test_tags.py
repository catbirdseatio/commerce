import pytest

from django.template import Template, Context


pytestmark = pytest.mark.django_db


class TestCategoryTags:
    def test_show_categories_five_categories_render(self, test_categories):
        template = Template(
            "{% load category_tags %}{% show_categories %}<h1>Hello</h1>"
        )
        rendered = template.render(Context({}))

        for category in test_categories:
            assert category.title in rendered
            assert category.get_absolute_url() in rendered

    def test_show_categories_zero_categories_render(self):
        categories = None
        template = Template(
            "{% load category_tags %}{% show_categories %}<h1>Hello</h1>"
        )
        rendered = template.render(Context({"categories": categories}))

        assert "There are no categories." in rendered

    def test_categories_card_five_categories_render(self, test_categories):
        template = Template(
            "{% load category_tags %}{% categories_card %}<h1>Hello</h1>"
        )
        rendered = template.render(Context({}))

        for category in test_categories:
            assert category.title in rendered
            assert category.get_absolute_url() in rendered

    def test_categories_card_zero_categories_render(self):
        categories = None
        template = Template(
            "{% load category_tags %}{% categories_card %}<h1>Hello</h1>"
        )
        rendered = template.render(Context({"categories": categories}))

        assert "There are no categories." in rendered
