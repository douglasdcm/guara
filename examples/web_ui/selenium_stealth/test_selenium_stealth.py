from guara.transaction import Application
from guara import it
from examples.web_ui.selenium_stealth import setup
from examples.web_ui.selenium_stealth import home
from random import randrange
from selenium import webdriver
from selenium_stealth import stealth


class TestSeleniumStealthIntegration:
    """
    TestSeleniumStealthIntegration is a test class for integrating
    Selenium Stealth with a local web page.
    """

    def setup_method(self, method):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=options)
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        self._app = Application(driver)
        self._app.at(
            setup.OpenStealthBrowser,
            url="https://example.com",
            window_width=1094,
            window_height=765,
            implicitly_wait=0.5,
        )

    def teardown_method(self, method):
        self._app.at(setup.CloseStealthBrowser)

    def test_local_page(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._app.at(home.SubmitSeleniumStealth, text=text).asserts(it.Contains, "Example Domain")
        self._app.at(home.SubmitSeleniumStealth, text=text).asserts(it.IsNotEqualTo, "Any")
