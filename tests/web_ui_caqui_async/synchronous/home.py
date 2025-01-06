from guara.transaction import AbstractTransaction
from tests.web_ui_caqui_async.constants import MAX_INDEX


class GetNthLink(AbstractTransaction):
    """
    Get the nth link from the page

    Args:
        link_index (int): The index of the link

    Returns:
        str: The nth link
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(
        self,
        link_index,
    ):
        locator_type = "xpath"
        locator_value = f"//a[@id='a{link_index}']"
        anchor = self._driver.find_element(locator_type, locator_value)
        return anchor.text


class GetAllLinks(AbstractTransaction):
    """
    Get the list of links from the page

    Returns:
        str: The list of links
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self):
        links = []
        max_index = MAX_INDEX - 1

        for i in range(max_index):
            i += 1
            links.append(
                # Instead of duplicate the code it is possible to call transactions directly
                GetNthLink(self._driver).do(
                    link_index=i,
                )
            )
        return links
