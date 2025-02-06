from pathlib import Path
from pytest import fixture
from selenium import webdriver
from examples.web_ui.selenium.advanced import home, contact, info
from guara.transaction import Application
from guara import it, setup

FILE_PATH = Path(__file__).parent.resolve()


class TestVpmTransaction:
    def setup_method(self, method):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self._app = Application(webdriver.Chrome(options=options))
        self._app.at(
            setup.OpenApp,
            url=f"file:///{FILE_PATH}/html/index.html",
        )

    def teardown_method(self, method):
        self._app.at(setup.CloseApp)

    def test_vpm_transaction_chain(self):
        text = "software testing"
        restricted_similariy = "Similarity 10.7%"
        expanded_similarity = "Similarity 15.4%"
        content_in_english = "Content of curriculum"
        content_in_portuguese = "Conteúdo do currículo"

        self._app.at(home.ChangeToPortuguese).asserts(it.IsEqualTo, content_in_portuguese)
        result = self._app.at(home.ChangeToEnglish).result
        it.IsEqualTo().asserts(result, content_in_english)
        self._app.at(info.NavigateTo).asserts(
            it.Contains,
            (
                "This project was born from the will of its collaborators to help"
                " people to find jobs more easily."
            ),
        )
        self._app.at(home.NavigateTo).asserts(it.IsEqualTo, content_in_english)
        self._app.at(contact.NavigateTo).asserts(
            it.IsEqualTo, "Contact us. We would be happy to answer your questions."
        )
        self._app.at(home.NavigateTo).asserts(it.IsEqualTo, content_in_english)
        self._app.at(home.DoRestrictedSearch, text=text, wait_for=restricted_similariy).asserts(
            it.IsEqualTo, restricted_similariy
        )
        self._app.at(home.NavigateTo).asserts(it.IsEqualTo, content_in_english)
        self._app.at(home.DoExpandedSearch, text=text, wait_for=expanded_similarity).asserts(
            it.IsEqualTo, expanded_similarity
        )
        self._app.at(home.NavigateTo).asserts(it.IsEqualTo, content_in_english)


@fixture
def setup_application():
    configuration = {
        "url": f"file:///{FILE_PATH}/html/index.html",
        "window_width": 1094,
        "window_height": 765,
        "implicitly_wait": 0.5,
    }
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    app = Application(webdriver.Chrome(options=options))
    app.at(setup.OpenApp, **configuration)
    yield app
    app.at(setup.CloseApp, screenshot_filename="./captures/guara-my-picture")


def test_vpm_transaction_builder(setup_application):
    app: Application = setup_application
    text = "software testing"
    restricted_similariy = "Similarity 10.7%"
    expanded_similarity = "Similarity 15.4%"
    content_in_english = "Content of curriculum"
    content_in_portuguese = "Conteúdo do currículo"

    app.at(home.ChangeToPortuguese).asserts(it.IsEqualTo, content_in_portuguese).at(
        home.ChangeToEnglish
    ).asserts(it.IsEqualTo, content_in_english).at(info.NavigateTo).asserts(
        it.Contains,
        (
            "This project was born from the will of its collaborators to"
            " help people to find jobs more easily."
        ),
    ).at(
        home.NavigateTo
    ).asserts(
        it.IsEqualTo, content_in_english
    ).at(
        contact.NavigateTo
    ).asserts(
        it.IsEqualTo, "Contact us. We would be happy to answer your questions."
    ).at(
        home.NavigateTo
    ).asserts(
        it.IsEqualTo, content_in_english
    ).at(
        home.DoRestrictedSearch, text=text, wait_for=restricted_similariy
    ).asserts(
        it.IsEqualTo, restricted_similariy
    ).at(
        home.NavigateTo
    ).asserts(
        it.IsEqualTo, content_in_english
    ).at(
        home.DoExpandedSearch, text=text, wait_for=expanded_similarity
    ).asserts(
        it.IsEqualTo, expanded_similarity
    ).at(
        home.NavigateTo
    ).asserts(
        it.IsEqualTo, content_in_english
    )
