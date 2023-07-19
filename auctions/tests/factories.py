from decimal import Decimal
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import factory
import factory.fuzzy

from auctions.models import Category, Listing, Bid


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'Testpass123')
    
    class Meta:
        model = User
        exclude = ('plaintext_password',)


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText(length=25)
    
    class Meta:
        model = Category


class ListingFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    description = factory.Faker(
        'paragraph', nb_sentences=3, variable_nb_sentences=True
    )
    seller = factory.SubFactory(UserFactory)
    starting_bid = factory.fuzzy.FuzzyDecimal(.01, 1000000, precision=2)
    is_active = factory.fuzzy.FuzzyChoice([True, False])
    category = factory.SubFactory(CategoryFactory)
    profile_image = factory.django.ImageField(color="red")

    class Meta:
        model = Listing


class BidFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    listing = factory.SubFactory(ListingFactory)
    bid_price = factory.LazyAttribute(lambda o: o.listing.current_price + Decimal(.01))
    
    class Meta:
        model = Bid