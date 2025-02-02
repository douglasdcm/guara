"""
The testing module that allows the testing of Selenium on
external pages.
"""

from pytest import fixture
from examples.web_ui.selenium.advanced import (
    home,
    contact,
    info,
)
from guara.transaction import Application
from guara.setup import OpenApp, CloseApp
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.options import Options
from guara.it import IsEqualTo, Contains
from typing import Any, Dict, Union, Generator


class TestVpmTransaction:
    def setup_method(self) -> None:
        options: Options = ChromeOptions()
        options.add_argument("--headless=new")
        self._app: Application = Application(Chrome(options=options))
        self._app.at(
            transaction=OpenApp,
            url="https://vagaspramim.onrender.com/",
        )

    def teardown_method(self) -> None:
        self._app.at(CloseApp)

    def test_vpm_transaction_chain(self) -> None:
        text: str = "software testing"
        restricted_similariy: str = "Similarity 10.7%"
        expanded_similarity: str = "Similarity 15.4%"
        content_in_english: str = "Content of curriculum"
        content_in_portuguese: str = "Conteúdo do currículo"
        self._app.at(home.ChangeToPortuguese).asserts(
            assertion=IsEqualTo,
            expected=content_in_portuguese,
        )
        result: Any = self._app.at(home.ChangeToEnglish).result
        IsEqualTo().asserts(result, content_in_english)
        self._app.at(home.ChangeToPortuguese).asserts(IsEqualTo, content_in_portuguese)
        # uses native assertion
        result = self._app.at(home.ChangeToEnglish).result
        IsEqualTo().asserts(result, content_in_english)
        self._app.at(info.NavigateTo).asserts(
            assertion=Contains,
            expected=(
                "This project was born from the will of its collaborators to help"
                " people to find jobs more easily."
            ),
        )
        self._app.at(home.NavigateTo).asserts(assertion=IsEqualTo, expected=content_in_english)
        self._app.at(contact.NavigateTo).asserts(
            assertion=IsEqualTo,
            expected="Contact us. We would be happy to answer your questions.",
        )
        self._app.at(home.NavigateTo).asserts(assertion=IsEqualTo, expected=content_in_english)
        self._app.at(home.NavigateTo).asserts(IsEqualTo, content_in_english)
        self._app.at(home.DoRestrictedSearch, text=text, wait_for=restricted_similariy).asserts(
            IsEqualTo, restricted_similariy
        )
        self._app.at(home.NavigateTo).asserts(IsEqualTo, content_in_english)
        self._app.at(home.DoExpandedSearch, text=text, wait_for=expanded_similarity).asserts(
            IsEqualTo, expanded_similarity
        )
        self._app.at(home.NavigateTo).asserts(IsEqualTo, content_in_english)


@fixture
def setup_application() -> Generator[Application, Any, None]:
    configuration: Dict[str, Union[str, int, float]] = {
        "url": "https://vagaspramim.onrender.com/",
        "window_width": 1094,
        "window_height": 765,
        "delay": 0.5,
    }
    options: Options = ChromeOptions()
    options.add_argument("--headless=new")
    app: Application = Application(Chrome(options=options))
    app.at(OpenApp, **configuration)
    yield app
    app.at(
        transaction=CloseApp,
        screenshot_filename="./captures/guara-my-picture",
    )


def test_vpm_transaction_builder(
    setup_application: Application,
) -> None:
    app: Application = setup_application
    text: str = "software testing"
    restricted_similariy: str = "Similarity 10.7%"
    expanded_similarity: str = "Similarity 15.4%"
    content_in_english: str = "Content of curriculum"
    content_in_portuguese: str = "Conteúdo do currículo"
    app.at(home.ChangeToPortuguese).asserts(assertion=IsEqualTo, expected=content_in_portuguese).at(
        home.ChangeToEnglish
    ).asserts(assertion=IsEqualTo, expected=content_in_english).at(info.NavigateTo).asserts(
        assertion=Contains,
        expected=(
            "This project was born from the will of its collaborators to"
            " help people to find jobs more easily."
        ),
    ).at(
        home.NavigateTo
    ).asserts(
        assertion=IsEqualTo, expected=content_in_english
    ).at(
        contact.NavigateTo
    ).asserts(
        assertion=IsEqualTo,
        expected="Contact us. We would be happy to answer your questions.",
    ).at(
        home.NavigateTo
    ).asserts(
        assertion=IsEqualTo, expected=content_in_english
    ).at(
        transaction=home.DoRestrictedSearch,
        text=text,
        wait_for=restricted_similariy,
    ).asserts(
        assertion=IsEqualTo, expected=restricted_similariy
    ).at(
        home.NavigateTo
    ).asserts(
        assertion=IsEqualTo, expected=content_in_english
    ).at(
        transaction=home.DoExpandedSearch,
        text=text,
        wait_for=expanded_similarity,
    ).asserts(
        assertion=IsEqualTo, expected=expanded_similarity
    ).at(
        home.NavigateTo
    ).asserts(
        assertion=IsEqualTo, expected=content_in_english
    )
