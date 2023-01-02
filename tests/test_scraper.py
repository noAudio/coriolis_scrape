from unittest import IsolatedAsyncioTestCase
from pyppeteer import launch

from c_scraper import coriolis_scrape


class TestCoriolisScraper(IsolatedAsyncioTestCase):
    async def launch_browser(self) -> None:
        self.browser = await launch()
        self.page = await self.browser.newPage()

    async def close_browser(self) -> None:
        await self.browser.close()

    async def test_coriolisScraper_gets_link(self) -> None:
        self.coriolisScraper = coriolis_scrape.CoriolisScraper(
            'https://s.orbis.zone/lgzu')

        self.assertEqual('https://s.orbis.zone/lgzu',
                         self.coriolisScraper.link)

    async def test_browser_opens_page(self) -> None:
        self.coriolisScraper = coriolis_scrape.CoriolisScraper(
            'https://s.orbis.zone/lgzu')

        # call method that gets the web page
        await self.coriolisScraper.openPage()
        self.assertIn('EasyChief', self.coriolisScraper.pageTitle)

    async def test_browser_can_identify_button(self) -> None:
        await self.launch_browser()
        # Open link of a coriolis ship build and check the correct page
        # is opened.
        await self.page.goto(url='https://s.orbis.zone/lgzu')
        self.pageTitle: str = await self.page.title()
        self.assertIn('EasyChief', self.pageTitle)

    async def test_scraper(self) -> None:
        self.coriolisScraper = coriolis_scrape.CoriolisScraper(
            'https://s.orbis.zone/lgzu')

        # call the method that identifies the button that generates
        # materials in json
        await self.coriolisScraper.getButton()
        self.assertIsNotNone(self.coriolisScraper.materialsButton)

    async def test_scraper_can_click_button(self) -> None:
        self.coriolisScraper = coriolis_scrape.CoriolisScraper(
            'https://s.orbis.zone/lgzu')

        # Identify button
        await self.coriolisScraper.getButton()

        # Click the button
        self.coriolisScraper.clickButton()
