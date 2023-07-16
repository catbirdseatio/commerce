import re
import uuid
import pytest
from auctions.models import User, Category, Listing


pytestmark = pytest.mark.django_db


class TestImage:
    def test_django_file(self, test_django_file):
        test_django_file.name = "test.jpeg"
        test_django_file.content = b"fileContent"
        test_django_file.content_type == "image/jpeg"


class TestListing:
    def test_listing_exists(self, test_listing):
        assert Listing.objects.count() == 1
    
    def test_listing_image_url_exists(self, test_listing):
        assert test_listing.profile_image is not None
        assert test_listing.profile_image.size > 1
    
    def test_listing_image_url_is_correct_format(self, test_listing):
        url = test_listing.profile_image.url.split("/")[1:]
        filename = url[-1].split(".")
        
        assert 'images' in url
        # check that the filename is uuid
        assert uuid.UUID(str(filename[0]))
    
    def test_image_preview(self, test_listing):
        assert test_listing.img_preview() == f'<img src="{test_listing.profile_image.url}" width="150" />'
        
    def test__str__(self, test_listing):
        assert test_listing.title == str(test_listing)