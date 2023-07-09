import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from pytest_django.asserts import assertTemplateUsed


pytestmark = pytest.mark.django_db

User = get_user_model()


class TestRegisterView:
    url = reverse("register")
    
    def test_page_success(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
    
    def test_page_template(self, client):
        response = client.get(self.url)
        assertTemplateUsed(response, "auctions/register.html")
    
    def test_successful_registration(self, client):
        data = {"username": "rodney", "email": "rodney@example.com", "password1": "Testpass123", "password2": "Testpass123"}
        response = client.post(self.url, data, follow_redirects=True)
        assert response.status_code == 302
        assert User.objects.filter(username="rodney").count() == 1
    
    def test_unsuccessful_registration(self, client, test_user):
        data = {"username": "rodney_boring", "email": "rodney@example.com", "password1": "Testpass123", "password2": "Testpass123"}
        response = client.post(self.url, data, follow_redirects=True)
        assert response.status_code == 200
        assert b"A user with that username already exists." in response.content