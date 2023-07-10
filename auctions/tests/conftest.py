import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from auctions.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(scope="function")
def test_django_file():
    image = SimpleUploadedFile("test.jpeg", b"fileContent", content_type="image/jpeg")
    # client.post(url, {'image_field_name': test_django_file})
    yield image


@pytest.fixture
def test_user():
    yield UserFactory(
        email="rodney@example.com",
        username="rodney_boring",
        is_superuser=False,
        is_staff=False,
        password="Testpass123",
    )


@pytest.fixture
def test_superuser():
    yield UserFactory(
        email="clarke@dailymail.com",
        is_superuser=True,
        is_staff=True,
        password="Testpass123",
    )


# @pytest.fixture()
# def new_user_factory(db):
#     def create_app_user(
#         username,
#         password=None,
#         first_name="firstname",
#         last_name="lastname",
#         email="firstname@example.com",
#         is_staff=False,
#         is_superuser=False,
#         is_active=True,
#     ):
#         user = User.objects.create_user(
#             username=username,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             is_staff=is_staff,
#             is_superuser=is_superuser,
#             is_active=is_active,
#         )
#         return user

#     yield create_app_user


# @pytest.fixture()
# def test_user(db, new_user_factory):
#     yield new_user_factory("clarke_kent", "testpass123", email="clarke@daily_planet.com", is_staff=True, is_superuser=True)
