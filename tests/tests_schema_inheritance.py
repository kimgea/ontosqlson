import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)


# TODO: schema should not be alowed to have a property that already exist in one of its ancestors


class TestSchemaInheritance(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_properties.clear()
        ontology.schema_models.clear()

    def test_schema_inheritance_basic(self):
        class NameThing(Schema):
            name = TextProperty()

        class NumberThing(NameThing):
            number = IntegerProperty()

        name_thing = NameThing()
        number_thing = NumberThing()

        self.assertIsNone(name_thing.name)
        name_thing.name = "name1"

        self.assertEqual(name_thing.name, "name1")

        self.assertIsNone(number_thing.name)
        self.assertIsNone(number_thing.number)
        number_thing.name = "name2"
        number_thing.number = 2

        self.assertEqual(number_thing.name, "name2")
        self.assertEqual(number_thing.number, 2)
        self.assertEqual(name_thing.name, "name1")

