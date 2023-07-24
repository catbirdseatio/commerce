import pytest
import string
import random
from auctions.forms import CommentForm


pytestmark = pytest.mark.django_db


class TestCommentForm:
    def test_valid_form(self, test_user, test_listing):
        content = ''.join(random.choices(string.ascii_lowercase +
            string.digits, k=1000))
        data = {'content': content, 'comment_form': True}
        form = CommentForm(data, user=test_user, listing=test_listing)
        print(form.errors)
        assert form.is_valid()
    
    def test_invalid_form(self, test_user, test_listing):
        content = ''.join(random.choices(string.ascii_lowercase +
            string.digits, k=1001))
        data = {'content': content, 'comment_form': True}
        form = CommentForm(data, user=test_user, listing=test_listing)
        assert not form.is_valid()
        
    
    def test_save(self, test_user, test_listing):
        content = ''.join(random.choices(string.ascii_lowercase +
            string.digits, k=1000))
        data = {'content': content, 'comment_form': True}
        form = CommentForm(data, user=test_user, listing=test_listing)
        form.is_valid()
        form.save()
        assert test_listing.comments.count() == 1