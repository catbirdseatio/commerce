import decimal
import random
import string
import json
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from pytest_django.asserts import assertTemplateUsed, assertContains
from auctions.models import Listing
from auctions.tests.factories import ListingFactory, BidFactory


pytestmark = pytest.mark.django_db

User = get_user_model()


class TestRegisterView:
    url = reverse("register")

    def test_get_success(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_page_template(self, client):
        response = client.get(self.url)
        assertTemplateUsed(response, "auctions/register.html")

    def test_successful_registration(self, client):
        data = {
            "username": "rodney",
            "email": "rodney@example.com",
            "password1": "Testpass123",
            "password2": "Testpass123",
        }
        response = client.post(self.url, data)
        assert response.status_code == 302
        assert User.objects.filter(username="rodney").count() == 1

    def test_unsuccessful_registration(self, client, test_user):
        data = {
            "username": test_user.username,
            "email": test_user.email,
            "password1": "Testpass123",
            "password2": "Testpass123",
        }
        response = client.post(self.url, data)
        assert response.status_code == 200
        assert b"A user with that username already exists." in response.content


class TestLoginView:
    url = reverse("login")

    def test_get_success(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_page_template(self, client):
        response = client.get(self.url)
        assertTemplateUsed(response, "auctions/login.html")

    def test_successful_login(self, test_user, client):
        data = {
            "username": test_user.username,
            "password": "Testpass123",
        }
        response = client.post(self.url, data)
        assert b"Invalid username and/or password." not in response.content
        assert response.status_code == 302

    def test_unsuccessful_login_200(self, test_user, client):
        data = {"username": "rodney", "password": "Password"}
        response = client.post(self.url, data)
        assert response.status_code == 200

    def test_unsuccessful_login_error_message(self, test_user, client):
        data = {"username": "rodney", "password": "Password"}
        response = client.post(self.url, data)
        assert b"Invalid username and/or password." in response.content

    def test_waitlist_link_is_not_zero(self, test_user, test_listing, client):
        test_listing.watchlist.add(test_user)

        data = {
            "username": test_user.username,
            "password": "Testpass123",
        }
        response = client.post(self.url, data, follow=True)
        assert (
            b'Watchlist <span class="badge rounded-pill bg-secondary px-3">'
            in response.content
        )

    def test_waitlist_link_is_zero(self, test_user, client):
        data = {
            "username": test_user.username,
            "password": "Testpass123",
        }
        response = client.post(self.url, data, follow=True)
        assert (
            b'Watchlist <span class="badge rounded-pill bg-secondary px-3">'
            in response.content
        )


class TestIndexView:
    url = reverse("index")

    def test_get_success(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_template_used(self, client):
        response = client.get(self.url)
        assertTemplateUsed(response, "auctions/index.html")

    def test_username_in_response(self, client, test_user):
        client.login(username=test_user.username, password="Testpass123")
        response = client.get(self.url)
        assert bytes(test_user.username, encoding="UTF-8") in response.content

    def test_cannot_post(self, client):
        response = client.post(self.url, {})
        assert response.status_code == 405

    def test_show_only_active_listings(self, client):
        for i in range(5):
            ListingFactory(is_active=False)

        for i in range(5):
            ListingFactory(is_active=True)

        response = client.get(self.url)
        assert response.status_code == 200
        assert len(response.context["listings"]) == 5


class TestWatchlistView:
    url = reverse("watchlist")

    def test_get_success(self, client, test_user):
        client.force_login(test_user)
        response = client.get(self.url)
        assert response.status_code == 200

    def test_get_anonymous_user_cannot_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 302

    def test_template_used(self, client, test_user):
        client.force_login(test_user)
        response = client.get(self.url)
        assertTemplateUsed(response, "auctions/watchlist.html")

    def test_cannot_post(self, client, test_user):
        client.force_login(test_user)
        response = client.post(self.url, {})
        assert response.status_code == 405

    def test_show_watched_listings(self, test_user, client):
        listings = [ListingFactory(is_active=False) for i in range(6)]

        for listing in listings:
            listing.watchlist.add(test_user)

        client.force_login(test_user)
        response = client.get(self.url)
        assert response.status_code == 200
        assert len(response.context["listings"]) == 6


class TestWatchlistAPIView:
    def url(self, pk):
        return reverse("watchlist_api", args=[pk])

    def test_watchlist_user_can_post(self, test_listing, test_user, client):
        client.force_login(test_user)
        response = client.post(self.url(test_listing.pk), {})
        assert response.status_code == 200
        assert (
            bytes(json.dumps({"message": "Item added to watchlist!"}), encoding="UTF-8")
            in response.content
        )

    def test_watchlist_user_added_to_watchlist(self, client, test_user, test_listing):
        url = self.url(test_listing.pk)
        client.force_login(test_user)
        response = client.post(url, {})
        assert test_user in test_listing.watchlist.all()

    def test_watchlist_user_can_delete(self, test_listing, test_user, client):
        client.force_login(test_user)
        response = client.delete(self.url(test_listing.pk), {})
        assert response.status_code == 200
        assert (
            bytes(
                json.dumps({"message": "Item removed from watchlist!"}),
                encoding="UTF-8",
            )
            in response.content
        )

    def test_watchlist_user_removed_from_watchlist(
        self, client, test_user, test_listing
    ):
        url = self.url(test_listing.pk)
        client.force_login(test_user)
        response = client.delete(url, {})
        assert test_user not in test_listing.watchlist.all()
        assert test_listing.watchlist.count() == 0

    def test_watchlist_user_removed_from_watchlist_failure(
        self, client, test_user, test_listing
    ):
        url = self.url(1000000000000000)
        client.force_login(test_user)
        response = client.delete(url, {})
        assert response.status_code == 404


class TestCreateView:
    url = reverse("create")

    def test_authenticated_user_can_get(self, client, test_user):
        client.login(username=test_user.username, password="Testpass123")
        response = client.get(self.url)
        assert response.status_code == 200

    def test_template_used(self, client, test_user):
        client.login(username=test_user.username, password="Testpass123")
        response = client.get(self.url)
        assertTemplateUsed(response, "auctions/create.html")

    def test_authenticated_user_can_post__with_image_success(
        self, client, test_user, valid_image
    ):
        client.login(username=test_user.username, password="Testpass123")
        response = client.post(
            self.url,
            data={
                "title": "Post Listing",
                "description": "A LISTING",
                "starting_bid": 1,
                "profile_image": valid_image,
            },
            follow=True,
        )
        assert b"The listing was successfully created." in response.content
        assert Listing.objects.filter(title="Post Listing").count() == 1

    def test_authenticated_user_can_post__without_image_success(
        self, client, test_user
    ):
        client.login(username=test_user.username, password="Testpass123")
        response = client.post(
            self.url,
            data={
                "title": "Post Listing",
                "description": "A LISTING",
                "starting_bid": 1,
            },
            follow=True,
        )
        assert b"The listing was successfully created." in response.content
        assert Listing.objects.filter(title="Post Listing").count() == 1

    def test_authenticated_user_can_post__without_image_failure(
        self, client, test_user
    ):
        client.login(username=test_user.username, password="Testpass123")
        response = client.post(
            self.url,
            data={
                "title": "Post Listing",
                "description": "A LISTING",
                "starting_bid": 0.01,
            },
            follow=True,
        )
        assert b"The listing was successfully created." not in response.content
        assert Listing.objects.filter(title="Post Listing").count() == 0

    def test_anonymous_user_cannot_get(self, client):
        response = client.get(self.url, follow_redirects=True)
        assert response.status_code == 302


class TestDetailView:
    def test_can_get(self, client, test_listing):
        response = client.get(test_listing.get_absolute_url())
        assert response.status_code == 200

    def test_template_used(self, client, test_listing):
        response = client.get(test_listing.get_absolute_url())
        assertTemplateUsed(response, "auctions/detail.html")

    def test_form_not_in_template_unauthenticated_user(self, client, test_listing):
        response = client.get(test_listing.get_absolute_url())
        assertContains(response, '<p class="mb-5">Log in to leave a comment.</p>')

    def test_display_high_bidder(self, client, test_listing):
        testing_bid = BidFactory(listing=test_listing)
        response = client.get(testing_bid.listing.get_absolute_url())
        assert bytes(f"There is 1 bid.", encoding="UTF-8") in response.content
        assert (
            bytes(f"{testing_bid.user} is the high bidder.", encoding="UTF-8")
            in response.content
        )

    def test_display_authenticated_user_is_high_bidder(
        self, client, test_listing, test_user
    ):
        testing_bid = BidFactory(listing=test_listing, user=test_user)
        client.force_login(test_user)
        response = client.get(testing_bid.listing.get_absolute_url())
        assert bytes(f"There is 1 bid.", encoding="UTF-8") in response.content
        assert bytes(f"You are the high bidder.", encoding="UTF-8") in response.content

    def test_display_high_bidder_inactive(self, client, test_inactive_listing):
        testing_bid = BidFactory(listing=test_inactive_listing)
        response = client.get(testing_bid.listing.get_absolute_url())
        assert bytes(f"The auction is over.", encoding="UTF-8") in response.content
        assert (
            bytes(f"{testing_bid.user} has won the auction.", encoding="UTF-8")
            in response.content
        )

    def test_display_user_is_high_bidder_inactive(
        self, client, test_inactive_listing, test_user
    ):
        testing_bid = BidFactory(listing=test_inactive_listing, user=test_user)
        client.force_login(test_user)
        response = client.get(testing_bid.listing.get_absolute_url())
        assert bytes(f"The auction is over.", encoding="UTF-8") in response.content
        assert bytes(f"You have won the auction.", encoding="UTF-8") in response.content

    def test_add_bid_success(self, client, test_user, test_listing):
        testing_bid = BidFactory(listing=test_listing)
        bid_price = decimal.Decimal(
            testing_bid.listing.current_price
        ) + decimal.Decimal(1)

        client.force_login(test_user)
        response = client.post(
            testing_bid.listing.get_absolute_url(),
            data={"bid_price": bid_price, "form": True},
            follow=True,
        )
        assert b"You are the high bidder!" in response.content
        assert test_listing.current_price == bid_price

    def test_add_bid_fail(self, client, test_user, test_listing):
        testing_bid = BidFactory(listing=test_listing)
        bid_price = testing_bid.listing.current_price

        client.force_login(test_user)
        response = client.post(
            testing_bid.listing.get_absolute_url(),
            data={"bid_price": bid_price, "form": True},
            follow_redirect=True,
        )
        assert b"Bid price must exceed current price" in response.content

    def test_add_bid_fail_new_listing(self, client, test_user, test_listing):
        client.force_login(test_user)
        bid_price = decimal.Decimal(test_listing.current_price) - decimal.Decimal(1)

        response = client.post(
            test_listing.get_absolute_url(),
            data={"bid_price": bid_price, "form": True},
            follow_redirect=True,
        )
        assert b"Bid must be greater than or equal to starting bid" in response.content

    def test_add_comment_success(self, client, test_user, test_listing):
        client.force_login(test_user)
        response = client.post(
            test_listing.get_absolute_url(),
            data={"content": "Hello There", "comment_form": True},
            follow=True,
        )
        assert b"Your comment has been added!" in response.content

    def test_anonymous_user_cannot_post(self, client, test_listing):
        response = client.post(
            test_listing.get_absolute_url(),
            data={"content": "Hello There", "comment_form": True},
        )
        assert response.status_code == 302

    def test_add_comment_fail_too_long(self, client, test_user, test_listing):
        content = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=1001)
        )
        client.force_login(test_user)
        response = client.post(
            test_listing.get_absolute_url(),
            data={"content": content, "comment_form": True},
        )
        assert b"Content exceeds 1000 characters." in response.content


class TestCategoryListView:
    def test_get_success(self, client, test_listing):
        category = test_listing.category
        url = category.get_absolute_url()
        response = client.get(url)
        assert response.status_code == 200

    def test_template_used(self, client, test_listing):
        category = test_listing.category
        url = category.get_absolute_url()
        response = client.get(url)
        assertTemplateUsed(response, "auctions/category.html")

    def test_cannot_post(self, client, test_listing):
        category = test_listing.category
        url = category.get_absolute_url()
        response = client.post(url)
        assert response.status_code == 405

    def test_get_category_view_context(self, client, test_listing):
        category = test_listing.category
        url = category.get_absolute_url()

        response = client.get(url)
        assert response.context["category"] == category.title
        assert len(response.context["listings"]) == 1
