from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCreateListingE2E:
    def test_form_submission_no_image(
        self, live_server, authenticated_browser, test_category, valid_image
    ):
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

        assert (
            "The listing was successfully created." in authenticated_browser.page_source
        )


class TestListingE2E:
    def test_username_in_navbar(
        self, live_server, authenticated_browser, test_listing, test_user
    ):
        authenticated_browser.get(
            f"{live_server.url}/{test_listing.get_absolute_url()}"
        )
        username = authenticated_browser.find_element(By.TAG_NAME, "strong")
        assert test_user.username == username.text

    def test_logout_in_navbar(
        self, live_server, authenticated_browser, test_listing, test_user
    ):
        authenticated_browser.get(
            f"{live_server.url}/{test_listing.get_absolute_url()}"
        )
        assert "Log Out" in authenticated_browser.page_source

    def test_add_watchlist_button_in_page(self, live_server, authenticated_browser, test_listing):
        authenticated_browser.get(
            f"{live_server.url}/{test_listing.get_absolute_url()}"
        )
        
        add_watchlist_button = authenticated_browser.find_element(By.ID, 'watchlist-button')
        assert add_watchlist_button.text == "Add to Watchlist"
    
    def test_remove_watchlist_button_in_page(self, live_server, authenticated_browser, test_listing, test_user):
        test_listing.watchlist.add(test_user)
        authenticated_browser.get(
            f"{live_server.url}/{test_listing.get_absolute_url()}"
        )
        
        add_watchlist_button = authenticated_browser.find_element(By.ID,'watchlist-button')
        assert add_watchlist_button.text == "Remove from Watchlist"
    
    def test_add_watchlist_button_clicked(self, live_server, authenticated_browser, test_listing):
        authenticated_browser.get(
            f"{live_server.url}/{test_listing.get_absolute_url()}"
        )
        
        add_watchlist_button = authenticated_browser.find_element(By.ID,
            'watchlist-button')
        watchlist_badge = authenticated_browser.find_element(By.CSS_SELECTOR, '#watchlist-link > .badge')
        watchlist_badge_value = int(watchlist_badge.text)
        
        authenticated_browser.execute_script('arguments[0].click();', add_watchlist_button)

        assert str(watchlist_badge_value + 1)  == watchlist_badge.text
        assert "Item added to watchlist!" in authenticated_browser.page_source

    def test_remove_watchlist_button_clicked(self, live_server, authenticated_browser, test_listing, test_user):
        test_listing.watchlist.add(test_user)
        authenticated_browser.get(
            f"{live_server.url}/{test_listing.get_absolute_url()}"
        )
        
        add_watchlist_button = authenticated_browser.find_element(By.ID,
            'watchlist-button')
        watchlist_badge = authenticated_browser.find_element(By.CSS_SELECTOR, '#watchlist-link > .badge')
        watchlist_badge_value = int(watchlist_badge.text)
        
        authenticated_browser.execute_script('arguments[0].click();', add_watchlist_button)

        assert str(watchlist_badge_value - 1)  == watchlist_badge.text
        assert "Item removed watchlist!" in authenticated_browser.page_source
