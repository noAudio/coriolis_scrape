from typing import List

from c_scraper.materials_model import Material
from c_scraper.coriolis_scrape import CoriolisScraper


class ListBuilder:
    link: str
    materialsData: List[Material]
    generalMaterials: str
    specialMaterials: List[str]
    shipName: str
    buildName: str
    completeMaterialsData: str  # Hold list of materials as json

    def __init__(self, link: str) -> None:
        self.link = link

    async def generateData(self) -> None:
        '''Calls the Coriolis scraper and generates the raw data from the site's json response.
        '''
        self.scraper = CoriolisScraper(link=self.link)

        await self.scraper.getMaterials()
        await self.scraper.getRawExperimentalsMaterials()

        self.generalMaterials = self.scraper.materialsAsText
        self.specialMaterials = self.scraper.experimentalsMaterials
        self.buildName = self.scraper.buildName
        self.shipName = self.scraper.shipName
