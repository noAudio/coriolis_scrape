from typing import Dict
from pyppeteer import launch, element_handle
from time import sleep


class CoriolisScraper:
    link: str  # link to coriolis build
    pageTitle: str
    materialsButton: element_handle.ElementHandle | None
    materialsHTMLElement: element_handle.ElementHandle | None
    errorMsg: str
    materialsAsText: str
    materials: Dict[str, str]

    def __init__(self, link: str) -> None:
        self.link = link

    async def setupBrowser(self) -> None:
        # TODO: Go back to headless mode
        self.browser = await launch({"autoClose": False, "headless": False})
        self.page = await self.browser.newPage()

    async def closeBrowser(self) -> None:
        await self.browser.close()

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

    async def clickButton(self) -> None:
        # Identify the button
        await self.getButton()

        # Click the button
        await self.materialsButton.click()

    async def getMaterialsHTMLElement(self) -> None:
        # Click button that generates materials
        await self.clickButton()

        # Identify element that holds the materials in text and assign
        # to `materials`
        self.materialsHTMLElement = await self.page.querySelector('#coriolis > div > div.modal-bg > div > div > textarea')

    async def getMaterials(self) -> None:
        await self.getMaterialsHTMLElement()

        # Get the innerHTML text
        if (self.materialsHTMLElement == None):
            self.errorMsg = 'Unable to get rendered textarea that contains HTML element'
            print(self.errorMsg)
        self.materialsAsTextJsonValue = await self.materialsHTMLElement.getProperty('textContent')
        self.materialsAsText = await self.materialsAsTextJsonValue.jsonValue()
