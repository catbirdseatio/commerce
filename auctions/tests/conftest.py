import pytest
from io import BytesIO
import decimal
import random
import string
from PIL import Image as img
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from selenium import webdriver

from auctions.tests.factories import (
    CategoryFactory,
    UserFactory,
    ListingFactory,
    BidFactory,
)
from auctions.forms import CommentForm, BidForm


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
    image = img.new("RGBA", size=(50, 50), color=(155, 0, 0))
    image.save(image_file, "png")
    image_file.name = "test_image.png"
    image_file.seek(0)
    return image_file


@pytest.fixture
def test_user():
    return UserFactory()


@pytest.fixture
def test_category():
    return CategoryFactory()


@pytest.fixture
def test_categories():
    return [CategoryFactory() for _ in range(5)]


@pytest.fixture
def test_listing(scope="function"):
    return ListingFactory(is_active=True)


@pytest.fixture
def test_inactive_listing():
    return ListingFactory(is_active=False)


@pytest.fixture
def imageless_listing():
    return ListingFactory(is_active=True, profile_image=None)


@pytest.fixture
def testing_bid():
    return BidFactory()


# Form fixtures
@pytest.fixture(scope="function")
def bid_form(test_listing, test_user):
    bid_price = decimal.Decimal(test_listing.current_price) + decimal.Decimal(".01")
    data = {"bid_price": bid_price, "form": True}

    return BidForm(data, user=test_user, listing=test_listing)


@pytest.fixture(scope="function")
def invalid_bid_form(test_listing, test_user):
    bid_price = decimal.Decimal(test_listing.current_price) - decimal.Decimal(".01")
    data = {"bid_price": bid_price, "form": True}

    return BidForm(data, user=test_user, listing=test_listing)


@pytest.fixture(scope="function")
def comment_form(test_listing, test_user):
    content = "".join(random.choices(string.ascii_lowercase + string.digits, k=1000))
    data = {"content": content, "comment_form": True}
    return CommentForm(data, user=test_user, listing=test_listing)


@pytest.fixture(scope="function")
def invalid_comment_form(test_listing, test_user):
    content = "".join(random.choices(string.ascii_lowercase + string.digits, k=1001))
    data = {"content": content, "comment_form": True}
    return CommentForm(data, user=test_user, listing=test_listing)


# Selenium fixtures
@pytest.fixture(scope="module")
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()


@pytest.fixture
def authenticated_browser(browser, client, live_server, test_user):
    client.force_login(test_user)
    cookie = client.cookies["sessionid"]
    browser.get(live_server.url)
    browser.add_cookie(
        {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
    )
    browser.refresh()

    return browser
