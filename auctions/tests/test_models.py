import pytest
from auctions.models import User


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
