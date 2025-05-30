# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction
from caqui import asynchronous


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
