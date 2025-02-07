# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pathlib import Path
from random import randrange
from guara.transaction import Application
from guara import it
from examples.web_ui.helium import setup
from examples.web_ui.helium import home


class TestHeliumIntegration:
    def setup_method(self, method):
        file_path = Path(__file__).parent.parent.resolve()

        self._app = Application(None)
        self._app.at(
            setup.OpenApp,
            url=f"file:///{file_path}/sample.html",
        )

    def teardown_method(self, method):
        self._app.at(setup.CloseApp)

    def test_local_page(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._app.at(home.SubmitText, text=text).asserts(it.IsEqualTo, f"It works! {text}!")
        self._app.at(home.SubmitText, text=text).asserts(it.IsNotEqualTo, "Any")
