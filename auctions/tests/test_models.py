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
        print(f"FIRST_NAME:{test_user.first_name} LAST_NAME: {test_user.last_name} EMAIL: {test_user.email}")
        assert User.objects.count() == 1

    def test_assert_superuser(self, test_superuser):
        print(f"FIRST_NAME:{test_superuser.first_name} LAST_NAME: {test_superuser.last_name} EMAIL: {test_superuser.email}")
        assert test_superuser.email == "clarke@dailymail.com"
        assert test_superuser.is_superuser is True
        assert test_superuser.is_staff is True
