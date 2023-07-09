import os
import pytest
from io import BytesIO
from PIL import Image

from auctions.models import User


@pytest.fixture
def test_image(scope="function"):
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_image.png'
    file.seek(0)
    return file



@pytest.fixture()
def new_user_factory(db):
    def create_app_user(
        username,
        password=None,
        first_name="firstname",
        last_name="lastname",
        email="firstname@example.com",
        is_staff=False,
        is_superuser=False,
        is_active=True,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        return user

    yield create_app_user


@pytest.fixture()
def test_user(db, new_user_factory):
    yield new_user_factory("clarke_kent", "testpass123", email="clarke@daily_planet.com", is_staff=True, is_superuser=True)
