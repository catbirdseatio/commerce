import pytest
from io import BytesIO
from PIL import Image as img
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from auctions.models import Listing


DESCRIPTION = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean aliquam nisi ac ipsum lobortis facilisis.
Aliquam nec dui vel arcu luctus aliquet. Fusce in dolor nulla. Nullam cursus et nunc id euismod. Donec eget sem vel sem aliquet ornare eget non augue. 
Vivamus id lorem viverra, pellentesque ante eu, elementum felis. Nullam porttitor sem in nulla accumsan, quis sagittis mauris cursus. Cras orci est, condimentum eget rhoncus nec, sodales non odio.
"""


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
def test_user(db):
    yield get_user_model().objects.create_user(
        username="testuser", email="test@example.com", password="Testpass123"
    )


@pytest.fixture
def test_listing(db, test_user, test_django_file):
    yield Listing.objects.create(title="A Listing",
    description=DESCRIPTION,
    seller=test_user,
    starting_bid=1.25,
    profile_image =test_django_file)


@pytest.fixture
def imageless_listing(db, test_user):
    yield Listing.objects.create(title="An Imageless Listing",
    description=DESCRIPTION,
    seller=test_user,
    starting_bid=1.25)