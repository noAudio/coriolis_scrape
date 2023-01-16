from typing import Any, Dict, List
from pyppeteer import launch, element_handle

import json


class CoriolisScraper:
    link: str  # link to coriolis build
    pageTitle: str
    materialsButton: element_handle.ElementHandle | None
    materialsHTMLElement: element_handle.ElementHandle | None
    errorMsg: str
    shipName: str
    buildName: str
    materialsAsText: str
    materials: Dict[str, str]
    experimentalsMaterials: List[str] = []
    rawExperimentalsMaterials: Any

    def __init__(self, link: str) -> None:
        self.link = link

    async def setupBrowser(self) -> None:
        # TODO: Go back to headless mode
        self.browser = await launch(
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False
        )
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

        self.materialsAsTextJsonValue = await self.materialsHTMLElement.getProperty('textContent')
        self.materialsAsText = await self.materialsAsTextJsonValue.jsonValue()

    def getSpecials(self, componentsSection: Dict[Any, Any]):
        # Iterate over keys and values in the first nested dictionary
        for key, value in componentsSection.items():
            if isinstance(value, dict):
                # Check for a nested dictionary and then check if its
                # the dictionary that holds the entries we need, then add
                # them to a list.
                if key == 'special':
                    for k, v in value['components'].items():
                        self.experimentalsMaterials.append(f'{k}: {v}')
                # Throw the dictionary back into this function to check the
                # other nested dictionaries for the required data
                self.getSpecials(value)
            else:
                # Some of the entries will be lists. We need to check for
                # that then iterate over the nested dictionaries in the list
                # to get the data
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            self.getSpecials(item)

    def getShipAndOrBuildName(self, jsonData: Dict[Any, Any]) -> None:
        self.shipName = jsonData['ship']
        if jsonData['name']:
            self.buildName = jsonData['name']

    async def getRawExperimentalsMaterials(self) -> None:
        ''' Open page and then click the 'Export' button to get the json for the full build details.
        '''
        await self.openPage()

        # Check that the button that generates ship build json is
        # rendered.
        try:
            self.exportButton = await self.page.querySelector('#build > button:nth-child(7)')
        except:
            self.errorMsg = 'Unable to locate export button'

        await self.exportButton.click()

        # Check for the Export json modal
        self.exportJsonModal = await self.page.querySelector('#coriolis > div > div.modal-bg > div > div:nth-child(3) > textarea')

        self.rawData = await self.exportJsonModal.getProperty(
            'textContent')
        self.jsonOutput = await self.rawData.jsonValue()

        self.rawExperimentalsMaterials = json.loads(self.jsonOutput)

        # Evaluate json and get ship name and, if available, build name
        self.getShipAndOrBuildName(self.rawExperimentalsMaterials)

        # Evaluate json and extract materials.
        self.getSpecials(self.rawExperimentalsMaterials['components'])
