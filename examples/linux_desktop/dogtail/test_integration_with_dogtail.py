from pytest import mark
from guara.transaction import Application


@mark.skip(reason="Complex setup in CI environment")
class TestLinuxCalculatorWithDogtail:
    def setup_method(self, method):
        # Opted for lazy import just to not break the pipeline
        # Do not do it
        from dogtail.tree import root
        from dogtail.procedural import run, focus
        from examples.linux_desktop.dogtail.screens import setup

        # Dogtail first runs the app and then gets the application.
        # So the calculator is opened direclty in the fixture.
        # This is an exception when compared against with other drivers like Selenium
        # that first gets the driver and then opens the app
        app_name = "gnome-calculator"
        run(app_name)
        focus.application(app_name)
        driver = root.application("gnome-calculator")

        self._calculator = Application(driver=driver)
        self._calculator.at(
            setup.OpenApp,
        )

    def teardown_method(self, method):
        from examples.linux_desktop.dogtail.screens import setup

        self._calculator.at(setup.CloseApp)

    @mark.parametrize("a,b,expected", [(1, 2, 3), (3, 5, 8), (0, 0, 0), (9, 1, 10)])
    def test_calculator_with_dogtail(self, a, b, expected):
        from examples.linux_desktop.dogtail.screens import calculator
        from examples.linux_desktop.dogtail.assertions import this

        self._calculator.at(calculator.Sum, a=a, b=b).asserts(this.Shows, expected)
