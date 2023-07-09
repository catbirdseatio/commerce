from auctions.models import User


class TestImage:
    def test_image(self, test_image):
        # image -> raw bytes.
        image = test_image.read()
        assert test_image is not None
        assert len(image) == 145
        assert test_image.name == 'test_image.png'


class TestUser:
    def test_user_creation(self, test_user):
        assert User.objects.count() == 1

    def test_assert_superuser(self, test_user):
        assert test_user.email == "clarke@daily_planet.com"
        assert test_user.is_superuser is True