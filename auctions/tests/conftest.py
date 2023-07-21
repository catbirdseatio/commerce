import pytest
from io import BytesIO
from PIL import Image as img
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from selenium import webdriver

from auctions.tests.factories import CategoryFactory, UserFactory, ListingFactory, BidFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture(scope="function")
def test_django_file():
    image = SimpleUploadedFile("test.jpeg", b"000000", content_type="image/jpeg")
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


# Selenium fixtures
@pytest.fixture(scope='module')
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def authenticated_browser(browser, client, live_server, test_user):
    client.force_login(test_user)
    cookie = client.cookies['sessionid']
    browser.get(live_server.url)
    browser.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/'
    })
    browser.refresh()
    
    return browser