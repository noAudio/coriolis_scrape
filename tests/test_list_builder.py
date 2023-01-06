from unittest import IsolatedAsyncioTestCase

from c_scraper.list_builder import ListBuilder


class TestListBuilder(IsolatedAsyncioTestCase):
    testLink: str = 'https://s.orbis.zone/lgzu'

    async def test_list_builder_can_get_materials(self) -> None:
        self.listBuilder: ListBuilder = ListBuilder(link=self.testLink)

        await self.listBuilder.generateData()

        self.assertTrue(self.listBuilder.materialsData)
