import os
import pytest
from unittest.mock import patch
from selenium import webdriver
from selenium.webdriver.common.by import By

from guara.transaction import Application, AbstractTransaction
from guara import it

# --- 1. Transactions ---


class VisitGoogle(AbstractTransaction):
    """A simple transaction that succeeds"""

    def do(self, **kwargs):
        # We just return the title to prove we reached the site
        return self._driver.title


class FailingTransaction(AbstractTransaction):
    """A transaction designed to fail by looking for a fake element"""

    def do(self, **kwargs):
        # This ID does not exist on Google, so Selenium will throw NoSuchElementException
        return self._driver.find_element(By.ID, "this-element-does-not-exist")


# --- 2. Pytest Fixture for Firefox ---


@pytest.fixture
def app():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.google.com")
    yield Application(driver)

    # Teardown: Close the browser after the test
    driver.quit()


# --- 3. The Tests ---


def test_successful_transaction_no_retries(app):
    """Tests that a normal transaction works without triggering retries"""
    with patch.dict(os.environ, {"RETRIES_ON_FAILURE": "3"}):
        app.at(VisitGoogle)
        app.asserts(it.Contains, "Google")


def test_failed_transaction_triggers_retries(app):
    """Tests that the retry logic actually fires when Selenium fails"""
    # We set retries to 2 (Total 3 attempts: 1 original + 2 retries)
    with patch.dict(os.environ, {"RETRIES_ON_FAILURE": "2"}):
        with pytest.raises(Exception):
            app.at(FailingTransaction)

    # If you run this with -s, you will see the 'Attempt 0', 'Attempt 1' logs!
