import asyncio

from flask import Flask, render_template
from c_scraper.list_builder import ListBuilder

loop = asyncio.get_event_loop()
app: Flask = Flask(__name__)


async def generateMaterials(coriolisLink: str) -> str:
    matList: ListBuilder = ListBuilder(
        link=f'https://s.orbis.zone/{coriolisLink}')

    await matList.generateData()
    matList.convertAllDataToMaterialObjects()

    return matList.toJson()


@app.route('/')
def index():
    '''This route will return the home page of the app.
    '''
    return 'render_template("index.html")'


@app.route('/generate/<coriolisLink>')
def generate(coriolisLink: str) -> str:
    '''This route will return the generated materials based on the
    given link.
    '''
    materialsJson: str = loop.run_until_complete(
        generateMaterials(coriolisLink=coriolisLink))

    return materialsJson


if __name__ == '__main__':
    app.run(debug=False)
