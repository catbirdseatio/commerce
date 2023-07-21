from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class TestCreateListingE2E:
    def test_form_submission_no_image(self, live_server, authenticated_browser, test_category, valid_image):
        authenticated_browser.get(f"{live_server.url}{reverse('create')}")

        title = authenticated_browser.find_element(By.NAME, "title")
        description = authenticated_browser.find_element(By.NAME, "description")
        starting_bid = authenticated_browser.find_element(By.NAME, "starting_bid")
        category = authenticated_browser.find_element(By.NAME, "category")
        select_category = Select(category)
        submit = authenticated_browser.find_element(By.XPATH, "//input[@type='submit']")

        title.send_keys("An Item")
        description.send_keys("lorem ipsum de facto.")
        starting_bid.send_keys(".01")
        select_category.select_by_index(0)
        submit.submit()
        
        assert "The listing was successfully created." in authenticated_browser.page_source

class TestListingE2E:
    def test_username_in_navbar(self, live_server, authenticated_browser, test_listing, test_user):
        authenticated_browser.get(f"{live_server.url}/{test_listing.get_absolute_url()}")
        username = authenticated_browser.find_element(By.TAG_NAME, "strong")
        assert test_user.username == username.text
    
    def test_logout_in_navbar(self, live_server, authenticated_browser, test_listing, test_user):
        authenticated_browser.get(f"{live_server.url}/{test_listing.get_absolute_url()}")
        nav_links = authenticated_browser.find_elements(By.CLASS_NAME, "nav-link")
        
        # Link text must be extracted into a list
        links = [link.text for link in nav_links]
        assert "Log Out" in links

        