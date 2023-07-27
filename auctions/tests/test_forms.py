import pytest
import string
import random

from auctions.forms import CommentForm, BidForm


pytestmark = pytest.mark.django_db


class TestCommentForm:
    def test_valid_form(self, comment_form):
        assert comment_form.is_valid()

    def test_invalid_form(self, invalid_comment_form):
        assert not invalid_comment_form.is_valid()

    def test_save(self, comment_form, test_listing):
        comment_form.is_valid()
        instance = comment_form.save()
        assert test_listing.comments.count() == 1
        assert int(instance.pk)

    def test_save_no_commit(self, comment_form, test_listing):
        comment_form.is_valid()
        instance = comment_form.save(commit=False)
        assert test_listing.comments.count() == 0
        assert instance is not None
        assert instance.pk is None


class TestBidForm:
    def test_valid_form(self, bid_form):
        assert bid_form.is_valid()

    def test_invalid_bid_form(self, invalid_bid_form):
        assert not invalid_bid_form.is_valid()

    def test_save(self, bid_form, test_listing):
        instance = bid_form.save()
        assert test_listing.bids.count() == 1
        assert int(instance.pk)

    def test_save_no_commit(self, bid_form, test_listing):
        bid_form.is_valid()
        instance = bid_form.save(commit=False)
        assert test_listing.comments.count() == 0
        assert instance is not None
        assert instance.pk is None
