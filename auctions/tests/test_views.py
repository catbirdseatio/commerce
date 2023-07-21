import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from pytest_django.asserts import assertTemplateUsed
from auctions.models import Listing
from auctions.tests.factories import ListingFactory


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
        assert len(response.context['listings']) == 5

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
    
    def test_authenticated_user_can_post__with_image_success(self, client, test_user, valid_image):
        client.login(username=test_user.username, password="Testpass123")
        response = client.post(self.url, data={"title" : "Post Listing", "description": "A LISTING", "starting_bid": 1, "profile_image": valid_image}, follow=True)
        assert b"The listing was successfully created." in response.content
        assert Listing.objects.filter(title="Post Listing").count() == 1
    
    def test_authenticated_user_can_post__without_image_success(self, client, test_user):
        client.login(username=test_user.username, password="Testpass123")
        response = client.post(self.url, data={"title" : "Post Listing", "description": "A LISTING", "starting_bid": 1}, follow=True)
        assert b"The listing was successfully created." in response.content
        assert Listing.objects.filter(title="Post Listing").count() == 1
    
    def test_anonymous_user_cannot_get(self, client):
        response = client.get(self.url, follow_redirects=True)
        assert response.status_code == 302
        