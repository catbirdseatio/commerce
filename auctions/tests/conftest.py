import pytest
from io import BytesIO
from PIL import Image as img
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from auctions.tests.factories import CategoryFactory, UserFactory, ListingFactory, BidFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(scope="function")
def test_django_file():
    image = SimpleUploadedFile("test.jpeg", b"000000", content_type="image/jpeg")
    # client.post(url, {'image_field_name': test_django_file})
    yield image


@pytest.fixture
def valid_image():
    """Helper to for creating test image for view tests."""
    image_file = BytesIO()
    image = img.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(image_file, 'png')
    image_file.name = 'test_image.png'
    image_file.seek(0)
    return image_file



@pytest.fixture
def test_user():
    return UserFactory()


@pytest.fixture
def test_category():
    return CategoryFactory()


@pytest.fixture
def test_listing():
    return ListingFactory()


@pytest.fixture
def imageless_listing():
    return ListingFactory(profile_image=None)

@pytest.fixture
def testing_bid():
    return BidFactory()