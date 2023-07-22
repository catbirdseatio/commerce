import re
import uuid
import pytest
from auctions.models import User, Category, Listing
from auctions.tests.factories import BidFactory


pytestmark = pytest.mark.django_db


class TestImage:
    def test_django_file(self, test_django_file):
        test_django_file.name = "test.jpeg"
        test_django_file.content = b"fileContent"
        test_django_file.content_type == "image/jpeg"


class TestCategory:
    def test__str__(self, test_category):
        assert test_category.title == str(test_category)
        assert test_category.__str__() == test_category.title


class TestUser:
    def test__str__(self, test_user):
        assert test_user.username == str(test_user)
        assert test_user.__str__() == test_user.username


class TestListing:
    def test_listing_exists(self, test_listing):
        assert Listing.objects.count() == 1

    def test_listing_image_url_exists(self, test_listing):
        assert test_listing.profile_image is not None
        assert test_listing.profile_image.size > 1

    def test_listing_image_url_is_correct_format(self, test_listing):
        url = test_listing.profile_image.url.split("/")[1:]
        filename = url[-1].split(".")

        assert "images" in url
        # check that the filename is uuid
        assert uuid.UUID(str(filename[0]))

    def test_image_preview(self, test_listing):
        assert (
            test_listing.img_preview()
            == f'<img src="{test_listing.profile_image.url}" width="150" />'
        )

    def test_image_preview_no_profile_image(self, imageless_listing):
        assert imageless_listing.img_preview() is None

    def test__str__(self, test_listing):
        assert test_listing.title == str(test_listing)
        assert test_listing.__str__() == test_listing.title

    def test_user_current_price_is_starting_bid(self, test_listing):
        assert test_listing.starting_bid == test_listing.current_price

    def test_current_price_is_highest_bid(self, test_listing):
        bids = [BidFactory(listing=test_listing) for i in range(5)]

        bids[4].bid_price == test_listing.current_price

    def test_number_of_bids_is_zero(self, test_listing):
        assert test_listing.number_of_bids == 0

    def test_number_of_bids_is_one(self, test_listing):
        BidFactory(listing=test_listing)
        assert test_listing.number_of_bids == 1

    def test_number_of_bids_is_five(self, test_listing):
        for i in range(5):
            BidFactory(listing=test_listing)

        assert test_listing.number_of_bids == 5

    def test_high_bid(self, test_listing):
        bids = [BidFactory(listing=test_listing) for i in range(5)]
        assert test_listing.high_bid == bids[4]

    def test_high_bid_belongs_to_test_user(self, test_listing, test_user):
        for i in range(5):
            BidFactory(listing=test_listing)
        bid = BidFactory(listing=test_listing, user=test_user)
        assert test_listing.high_bid == bid

    def test_high_bid_is_none(self, test_listing):
        assert test_listing.high_bid is None

    def test_slug(self, test_listing):
        assert test_listing.slugify_function(test_listing.title) == test_listing.slug


class TestBid:
    def test__str__(self, testing_bid):
        bid_string = f"Bid #{testing_bid.id}: {testing_bid.bid_price}"
        assert testing_bid.__str__() == bid_string
        assert str(testing_bid) == bid_string
