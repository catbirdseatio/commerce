import pytest
from auctions.models import User, Category, Listing


pytestmark = pytest.mark.django_db


class TestImage:
    def test_django_file(self, test_django_file):
        test_django_file.name = "test.jpeg"
        test_django_file.content = b"fileContent"
        test_django_file.content_type == "image/jpeg"


class TestUser:
    def test_user_creation(self, test_user):
        assert User.objects.count() == 1

    def test_user__str__(self, test_user):
        username = test_user.username
        assert str(test_user) == username

    def test_assert_superuser(self, test_superuser):
        assert test_superuser.email == "clarke@dailymail.com"
        assert test_superuser.is_superuser is True
        assert test_superuser.is_staff is True


class TestCategory:
    def test_category_created(self, test_category):
        assert Category.objects.count() == 1

    def test__str__(self, test_category):
        assert test_category.title == str(test_category)


class TestListing:
    def test_listing_created(self, test_listing):
        assert Listing.objects.count() == 1
        
    def test__str__(self, test_listing):
        assert test_listing.title == str(test_listing)