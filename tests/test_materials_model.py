from typing import List
from unittest import TestCase

from c_scraper.materials_model import Material, materialsAsJson


class TestMaterial(TestCase):
    material: Material = Material(name='Iron', amount=5)

    def test_material_creation(self) -> None:
        self.material.amount = 5
        self.assertEqual(self.material.name, 'Iron')
        self.assertEqual(self.material.amount, 5)

    def test_material_amount_can_be_increased(self) -> None:
        self.material.increaseAmount(extraAmount=10)

        self.assertEqual(self.material.amount, 15)

    def test_material_conversion_to_string(self) -> None:
        self.material.amount = 5
        # Check that using the __str__() method returns a string
        self.assertEqual(type(self.material.__str__()), str)

        # Check that the returned string is in the required format
        self.assertEqual(self.material.__str__(), 'Iron: 5')

    def test_material_conversion_to_dictionary(self) -> None:
        self.material.amount = 5

        # Check the returned type is a dictionary
        self.assertEqual(type(self.material.toDict()), dict)

        # Check the returned dictionary matches the required format
        self.assertEqual(self.material.toDict(), {'Iron': 5})

    def test_materials_list_is_converted_to_json(self) -> None:
        # Test data
        materialsList: List[Material] = [
            Material(name='Molybdenum', amount=10),
            Material(name='Grid Resistors', amount=22),
            Material(name='Datamined Wake Exceptions', amount=40)
        ]

        self.jsonString: str = materialsAsJson(materials=materialsList)

        # Check type matches str and output matches required format
        self.assertEqual(type(self.jsonString), str)
        self.assertEqual(
            self.jsonString, '[{"Molybdenum": 10}, {"Grid Resistors": 22}, {"Datamined Wake Exceptions": 40}]',)
