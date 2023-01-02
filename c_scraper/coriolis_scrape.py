from typing import Any
from pyppeteer import launch, element_handle
from time import sleep


class CoriolisScraper:
    link: str  # link to coriolis build
    pageTitle: str
    materialsButton: element_handle.ElementHandle | None
    errorMsg: str

    def __init__(self, link: str) -> None:
        self.link = link

    async def setupBrowser(self) -> None:
        # TODO: Go back to headless mode
        self.browser = await launch({"autoClose": False, "headless": False})
        self.page = await self.browser.newPage()

    async def openPage(self) -> None:
        await self.setupBrowser()

        # Go to given link
        await self.page.goto(url=self.link)

        # Set page title
        self.pageTitle = await self.page.title()

    async def getButton(self) -> None:
        '''Locate the button that generates the materials json.

        If the button is found, it will be assigned to `materialsButton`, otherwise `None` will be assigned.
        '''
        await self.openPage()

        # Check the button that generates materials has been rendered
        try:
            self.materialsButton = await self.page.querySelector('#build > button:nth-child(10)')
        except:
            self.materialsButton = None
            self.errorMsg = 'Materials button not found'
