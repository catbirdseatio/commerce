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
        
    
class TestLoginView:
    url = reverse("login")
    
    def test_successful_login(self, test_user, client):
        data = {"username": "rodney", "password": "Testpass123"}
        response = client.post(self.url, data, follow_redirects=False)
        assert response.status_code == 200
    
    def test_unsuccessful_login_200(self, test_user, client):
        data = {"username": "rodney", "password": "Password"}
        response = client.post(self.url, data)
        assert response.status_code == 200
    
    def test_unsuccessful_login_error_message(self, test_user, client):
        data = {"username": "rodney", "password": "Password"}
        response = client.post(self.url, data)
        assert  b"Invalid username and/or password." in response.content
        

class TestIndexView:
    url = reverse("index")
    
    def test_can_get(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
    
    def test_template_used(self, client):
        response = client.get(self.url)
        assertTemplateUsed(response, "auctions/index.html")
    
    def test_username_in_response(self, client, test_user):
        client.force_login(test_user)
        response = client.get(self.url)
        print(response.content)
        assert bytes(test_user.username, encoding="UTF-8") in response.content