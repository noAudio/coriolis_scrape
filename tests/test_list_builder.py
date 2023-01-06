from typing import List
from unittest import IsolatedAsyncioTestCase

from c_scraper.list_builder import ListBuilder
from c_scraper.materials_model import Material


class TestListBuilder(IsolatedAsyncioTestCase):
    testLink: str = 'https://s.orbis.zone/lgzu'
    experimentalsTestData: List[str] = [
        'Grid Resistors: 5', 'Vanadium: 3', 'Polymer Capacitors: 1', 'Iron: 5', 'Hybrid Capacitors: 3', 'Security Firmware Patch: 1', 'Atypical Disrupted Wake Echoes: 5', 'Galvanising Alloys: 3', 'Eccentric Hyperspace Trajectories: 1', 'Phosphorus: 5', 'Heat Resistant Ceramics: 3', 'Security Firmware Patch: 1', 'Mechanical Scrap: 5', 'Mechanical Components: 3', 'Ruthenium: 1', 'Mechanical Scrap: 5', 'Mechanical Components: 3', 'Ruthenium: 1', 'Mechanical Scrap: 5', 'Mechanical Components: 3', 'Ruthenium: 1', 'Heat Dispersion Plate: 5', 'Sulphur: 5', 'Tempered Alloys: 5', 'Mechanical Scrap: 5', 'Mechanical Components: 3', 'Ruthenium: 1',
        'Mechanical Scrap: 5', 'Mechanical Components: 3', 'Ruthenium: 1', 'Untypical Shield Scans: 3', 'Compact Composites: 5', 'Cadmium: 2', 'Untypical Shield Scans: 3', 'Compact Composites: 5', 'Cadmium: 2', 'Anomalous Bulk Scan Data: 5', 'Conductive Ceramics: 3', 'Heat Vanes: 3', 'Flawed Focus Crystals: 3', 'Worn Shield Emitters: 5', 'Conductive Polymers: 1', 'Chemical Storage Units: 5', 'Chromium: 3', 'Polymer Capacitors: 1', 'Chemical Storage Units: 5', 'Chromium: 3', 'Polymer Capacitors: 1', 'Compact Composites: 5', 'Molybdenum: 3', 'Ruthenium: 2', 'Compact Composites: 5', 'Heat Dispersion Plate: 3', 'Thermic Alloys: 2', 'Compact Composites: 5', 'Molybdenum: 3', 'Ruthenium: 2']
    generalMaterialsTestData: str = 'Nickel: 42'

    async def test_list_builder_can_get_materials(self) -> None:
        self.listBuilder: ListBuilder = ListBuilder(link=self.testLink)

        await self.listBuilder.generateData()

        self.assertTrue(
            self.generalMaterialsTestData in self.listBuilder.generalMaterials)
        self.assertTrue(self.listBuilder.specialMaterials ==
                        self.experimentalsTestData)
        self.assertTrue(self.listBuilder.shipName == 'Alliance Chieftain')
        self.assertTrue(self.listBuilder.buildName == 'EasyChief')

    async def test_data_is_converted_to_material_objects(self) -> None:
        self.listBuilder: ListBuilder = ListBuilder(link=self.testLink)

        await self.listBuilder.generateData()
        await self.listBuilder.convertDataToMaterialObjects()

        self.assertTrue(self.listBuilder.materialsData)
        self.assertEqual(type(self.listBuilder.materialsData[0]), Material)
