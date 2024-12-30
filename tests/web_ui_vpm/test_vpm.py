import pytest
from selenium import webdriver
from tests.web_ui_vpm import home, contact, info
from guara.transaction import Application
from guara import it, setup


class TestVpmTransaction:
    def setup_method(self, method):
        self._app = Application(webdriver.Chrome())
        self._app.at(
            setup.OpenApp,
            url="https://vagaspramim.onrender.com/",
        )

    def teardown_method(self, method):
        self._app.at(setup.CloseApp)

    def test_vpm_transaction_chain(self):
        text = "software testing"
        restricted_similariy = "Similarity 10.7%"
        expanded_similarity = "Similarity 15.4%"
        content_in_english = "Content of curriculum"
        content_in_portuguese = "Conteúdo do currículo"

        self._app.at(home.ChangeToPortuguese).asserts(
            it.IsEqualTo, content_in_portuguese
        )
        # uses native assertion
        assert self._app.at(home.ChangeToEnglish).result == content_in_english
        self._app.at(info.Navgigate).asserts(
            it.Contains,
            (
                "This project was born from the will of its collaborators to help"
                " people to find jobs more easily."
            ),
        )
        self._app.at(home.Navigate).asserts(it.IsEqualTo, content_in_english)
        self._app.at(contact.Navigate).asserts(
            it.IsEqualTo, "Contact us. We would be happy to answer your questions."
        )
        self._app.at(home.Navigate).asserts(it.IsEqualTo, content_in_english)
        self._app.at(
            home.DoRestrictedSearch, text=text, wait_for=restricted_similariy
        ).asserts(it.IsEqualTo, restricted_similariy)
        self._app.at(home.Navigate).asserts(it.IsEqualTo, content_in_english)
        self._app.at(
            home.DoExpandedSearch, text=text, wait_for=expanded_similarity
        ).asserts(it.IsEqualTo, expanded_similarity)
        self._app.at(home.Navigate).asserts(it.IsEqualTo, content_in_english)


@pytest.fixture
def setup_application():
    configuration = {
        "url": "https://vagaspramim.onrender.com/",
        "window_width": 1094,
        "window_hight": 765,
        "implicitly_wait": 0.5,
    }
    app = Application(webdriver.Chrome())
    app.at(setup.OpenApp, **configuration)
    yield app
    app.at(setup.CloseApp)


def test_vpm_transaction_builder(setup_application):
    app: Application = setup_application
    text = "software testing"
    restricted_similariy = "Similarity 10.7%"
    expanded_similarity = "Similarity 15.4%"
    content_in_english = "Content of curriculum"
    content_in_portuguese = "Conteúdo do currículo"

    app.at(home.ChangeToPortuguese).asserts(it.IsEqualTo, content_in_portuguese).at(
        home.ChangeToEnglish
    ).asserts(it.IsEqualTo, content_in_english).at(info.Navgigate).asserts(
        it.Contains,
        (
            "This project was born from the will of its collaborators to"
            " help people to find jobs more easily."
        ),
    ).at(
        home.Navigate
    ).asserts(
        it.IsEqualTo, content_in_english
    ).at(
        contact.Navigate
    ).asserts(
        it.IsEqualTo, "Contact us. We would be happy to answer your questions."
    ).at(
        home.Navigate
    ).asserts(
        it.IsEqualTo, content_in_english
    ).at(
        home.DoRestrictedSearch, text=text, wait_for=restricted_similariy
    ).asserts(
        it.IsEqualTo, restricted_similariy
    ).at(
        home.Navigate
    ).asserts(
        it.IsEqualTo, content_in_english
    ).at(
        home.DoExpandedSearch, text=text, wait_for=expanded_similarity
    ).asserts(
        it.IsEqualTo, expanded_similarity
    ).at(
        home.Navigate
    ).asserts(
        it.IsEqualTo, content_in_english
    )
