import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from auctions.tests.factories import UserFactory, CategoryFactory, ListingFactory


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


@pytest.fixture
def test_category():
    yield CategoryFactory(title="Musical Instruments")


@pytest.fixture
def test_listing(test_category, test_user):
    yield ListingFactory(seller=test_user, category=test_category)
