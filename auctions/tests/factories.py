from django.contrib.auth import get_user_model
from factory import  fuzzy, Faker, PostGenerationMethodCall, SubFactory
from factory.django import DjangoModelFactory
from auctions.models import Category, Listing


User = get_user_model()


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = PostGenerationMethodCall("set_password", "Testpass123")

    class Meta:
        model = User


class CategoryFactory(DjangoModelFactory):
    title = Faker("title")

    class Meta:
        model = Category


class ListingFactory(DjangoModelFactory):
    title = Faker("pystr")
    description = fuzzy.FuzzyText(length=300)
    seller = SubFactory(UserFactory)
    category = SubFactory(CategoryFactory)
    starting_bid = fuzzy.FuzzyDecimal(.01, 100000, 2)
    is_active = fuzzy.FuzzyChoice([True, False])
    class Meta:
        model = Listing
