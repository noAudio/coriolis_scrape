import asyncio
from c_scraper.list_builder import ListBuilder


async def scrapeItBoi():
    listB: ListBuilder = ListBuilder(link='https://s.orbis.zone/lgzu')

    await listB.generateData()


loop = asyncio.get_event_loop()
loop.run_until_complete(scrapeItBoi())
loop.close()
