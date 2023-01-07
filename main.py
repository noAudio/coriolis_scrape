import asyncio
from c_scraper.coriolis_scrape import CoriolisScraper
from c_scraper.list_builder import ListBuilder


async def scrapeItBoi():
    listB: ListBuilder = ListBuilder(link='https://s.orbis.zone/lgzu')

    await listB.generateData()
    listB.convertAllDataToMaterialObjects()
    print(listB.toJson())

    # scraper: CoriolisScraper = CoriolisScraper(
    #     link='https://s.orbis.zone/lgzu')

    # await scraper.getMaterials()
    # print(scraper.materialsAsTextJsonValue)
    # print(scraper.materialsAsText)


loop = asyncio.get_event_loop()
loop.run_until_complete(scrapeItBoi())
loop.close()
