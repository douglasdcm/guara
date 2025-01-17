import pytest


@pytest.mark.skip("Skipped due to the complexity to integrate it in pipeline")
class TestLinuxCalculatorWithPyautogui:

    def setup_method(self, method):
        # I opted for lazy imports just to not break the pipeline.
        # Do not do it.
        from guara.transaction import Application
        from screens import setup

        self._calculator = Application(driver=None)
        self._calculator.at(
            setup.OpenApp,
        )

    def teardown_method(self, method):
        from screens import setup

        self._calculator.at(setup.CloseApp)

    def test_calculator(self):
        from screens import calculator

        # Pyautogui seems not to enforce assertions. It also does not have a driver
        # which the tester could use to get information about the app. It just interacts
        # with whatever is shown in your host. One possible way to make assertions is
        # check if an specific image like `images/displays_3.png` is present in the screen
        # The tester has to be creative while asserting things with Pyautogui.
        # Other possible way is use dogtail to return information about the opened app.
        # In this case, dogtail has to be passed as the driver to the `Application`.
        # Check the examples in `examples/linux_desktop/dogtail` for more information.
        self._calculator.at(
            calculator.Add,
            a=1,
            b=2,
        )
