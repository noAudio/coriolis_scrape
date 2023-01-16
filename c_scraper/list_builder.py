import json
from typing import Dict, List

from c_scraper.materials_model import Material
from c_scraper.coriolis_scrape import CoriolisScraper


class ListBuilder:
    link: str
    materialsData: List[Material] = []
    generalMaterialsRaw: str
    generalMaterials: List[str]
    specialMaterials: List[str]
    shipName: str
    buildName: str | None
    completeMaterialsData: str  # Hold list of materials as json

    def __init__(self, link: str) -> None:
        self.link = link

    async def generateData(self) -> None:
        '''Calls the Coriolis scraper and generates the raw data from the site's json response.
        '''
        self.scraper = CoriolisScraper(link=self.link)

        await self.scraper.getMaterials()
        await self.scraper.getRawExperimentalsMaterials()

        self.generalMaterialsRaw = self.scraper.materialsAsText
        self.specialMaterials = self.scraper.experimentalsMaterials
        self.buildName = self.scraper.buildName
        self.shipName = self.scraper.shipName

    def cleanData(self) -> None:
        '''Convert the general materials from its original string format
        into a list of strings.
        '''
        # Turn general materials into a list of strings by splitting using
        # line break as the delimitter.
        self.splitData: List[str] = self.generalMaterialsRaw.split('\n')

        # Remove any empty strings
        for item in self.splitData:
            if item == '':
                self.splitData.remove(item)
        self.generalMaterials = self.splitData

    def convertData(self, data: List[str]) -> None:
        # Convert to Material object and append to list
        for item in data:
            item = item.split(': ')
            self.newMaterial: Material = Material(
                name=item[0], amount=int(item[1]))
            self.currentAmount: int
            self.duplicateIndex: int = -1
            # Check if the material is already added and if present then
            # increase its amount. Otherwise append the new material.
            if self.materialsData:
                for material in self.materialsData:
                    if self.newMaterial.name == material.name:
                        # Note the amount of the duplicate material and
                        # its index.
                        self.currentAmount = material.amount
                        self.duplicateIndex = self.materialsData.index(
                            material)
                if (self.duplicateIndex != -1):
                    # If there is an index for the duplicate material,
                    # remove it from the list.
                    self.materialsData.pop(self.duplicateIndex)
                    self.newMaterial.amount += self.currentAmount
                self.materialsData.append(self.newMaterial)
            else:
                self.materialsData.append(self.newMaterial)

    def convertAllDataToMaterialObjects(self) -> None:
        '''Converts the general materials and special materials into
        `Material` objects.
        '''
        self.cleanData()
        self.convertData(data=self.generalMaterials)
        self.convertData(data=self.specialMaterials)

    def toJson(self) -> str:
        '''The materials will be converted into json in the following
        format:
                `'shipName': 'Alliance Chieftain',`
                `'buildName': 'EasyChief',`
                `'coriolisLink': 'https://s.orbis.zone/lgzu',`
                `'materials': {`
                    `'Iron': 20,`
                    `'Classified Scan Databanks': 12,`
                    `'Grid Resistors': 45,`
                    `...`
                `}`
        '''
        if (not self.materialsData):
            return 'Error: Unable to generate materials, please reload.'

        # Create a dictionary to hold the data to be converted
        # Start by adding metadata (ship name, build name and the link used
        # to generate the data).
        self.dataObject: Dict[str, str | int | Dict[str, int] | bool] = {
            'shipName': self.shipName,
            'buildName': self.buildName or False,
            'coriolisLink': self.link,
            'materials': {}
        }

        self.materials: Dict[str, int] = {}

        for material in self.materialsData:
            self.materials.update(material.toDict())

        self.dataObject['materials'] = self.materials

        return json.dumps(self.dataObject)
