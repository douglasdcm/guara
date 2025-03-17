# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import fixture
from examples.web_ui.playwright.synchronous.pages import home, setup, getting_started
from guara.transaction import Application
from guara import it
from guara.utils import is_dry_run

if not is_dry_run():
    from playwright.sync_api import Page
else:

    @fixture
    def page():
        pass


@fixture
def setup_method(page):
    driver = None
    if not is_dry_run():
        driver = page

    app = Application(driver)
    app.at(
        setup.OpenApp,
        with_url="https://playwright.dev/",
    ).asserts(it.Contains, "Playwright")
    yield app


def test_local_page_playwright(setup_method):
    dev_page: Application = setup_method
    dev_page.at(home.NavigateToGettingStarted).asserts(it.IsEqualTo, "Installation")
    dev_page.at(getting_started.NavigateToWritingTests).asserts(it.IsNotEqualTo, "Writing Tests")
