import asyncio
from c_scraper.coriolis_scrape import CoriolisScraper


async def scrapeItBoi():
    scraper: CoriolisScraper = CoriolisScraper(
        link='https://s.orbis.zone/lgzu')

    await scraper.getRawExperimentalsMaterials()
loop = asyncio.get_event_loop()
loop.run_until_complete(scrapeItBoi())
loop.close()
