from caqui import asynchronous
from guara.transaction import AbstractTransaction
from tests.web_ui_caqui_async.constants import MAX_INDEX


class GetNthLink(AbstractTransaction):
    """
    Get the nth link from the page

    Args:
        link_index (int): The index of the link
        with_session (object): The session of the Web Driver
        connect_to_driver (str): The URL to connect the Web Driver server

    Returns:
        str: The nth link
    """

    def __init__(self, driver):
        super().__init__(driver)

    async def do(
        self,
        link_index,
        with_session,
        connect_to_driver,
    ):
        locator_type = "xpath"
        locator_value = f"//a[@id='a{link_index}']"
        anchor = await asynchronous.find_element(
            connect_to_driver, with_session, locator_type, locator_value
        )
        return await asynchronous.get_text(connect_to_driver, with_session, anchor)


class GetAllLinks(AbstractTransaction):
    """
    Get the list of links from the page

    Args:
        with_session (object): The session of the Web Driver
        connect_to_driver (str): The URL to connect the Web Driver server

    Returns:
        str: The list of links
    """

    def __init__(self, driver):
        super().__init__(driver)

    async def do(self, with_session, connect_to_driver):
        links = []
        max_index = MAX_INDEX - 1

        for i in range(max_index):
            i += 1
            links.append(
                # Instead of duplicate the code it is possible to call transactions directly
                await GetNthLink(None).do(
                    link_index=i,
                    with_session=with_session,
                    connect_to_driver=connect_to_driver,
                )
            )
        return links
