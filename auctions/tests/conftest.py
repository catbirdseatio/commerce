import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(scope="function")
def test_django_file():
    image = SimpleUploadedFile("test.jpeg", b"fileContent", content_type="image/jpeg")
    # client.post(url, {'image_field_name': test_django_file})
    yield image
