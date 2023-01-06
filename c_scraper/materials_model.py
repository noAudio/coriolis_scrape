from dataclasses import dataclass
from typing import Dict, List
import json


@dataclass
class Material:
    '''This is a data class for the engineering materials needed for a ship build.
    '''
    name: str
    amount: int

    def increaseAmount(self, extraAmount: int) -> None:
        # Increases the number of materials by the specified amount.
        self.amount = self.amount + extraAmount

    def __str__(self) -> str:
        return f'{self.name}: {self.amount}'

    def toDict(self) -> Dict[str, int]:
        '''Return material as dictionary object.
        '''
        return {self.name: self.amount}


def materialsAsJson(materials: List[Material]) -> str:
    '''Converts a list of `Material` objects into a serialised json string.
    The output will look like this:
        `[`
            `{"Iron": 4}`,
            `{"Molybdenum": 32}`,
            `{"Core Dynamic Components": 50}`,
            `{"Improvised Components": 25}`,
            `{"Military Supercapacitors": 12}`
        `]`
    '''
    materialsList: List[Dict[str, int]] = []

    for material in materials:
        materialsList.append(material.toDict())

    return json.dumps(materialsList)
