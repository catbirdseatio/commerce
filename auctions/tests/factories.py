from django.contrib.auth import get_user_model
from factory import Faker, PostGenerationMethodCall
from factory.django import DjangoModelFactory


User = get_user_model()


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = PostGenerationMethodCall("set_password", "Testpass123")

    class Meta:
        model = User
