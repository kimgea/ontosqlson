import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)


class TestSchemaLoad(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_properties.clear()
        ontology.schema_models.clear()

    def test_schema_load_basic(self):
        class Thing(Schema):
            name = TextProperty()
        thing = Thing()
        json_data = {"instance_of": "Thing", "name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")

    def test_schema_load_custom_property_name(self):
        class Thing(Schema):
            name = TextProperty(property_name="custom_name")
        thing = Thing()
        json_data = {"instance_of": "Thing", "custom_name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")

    def test_schema_load_schema_link(self):
        class Thing(Schema):
            name = TextProperty()

        class Thing2(Schema):
            other = ClassProperty("Thing")
        thing2 = Thing2()
        json_data = {"instance_of": "Thing2", "other": {"instance_of": "Thing", "name": "name1"}}
        self.assertIsNone(thing2.other)
        thing2.load(json_data)
        self.assertIsNotNone(thing2.other)
        self.assertEqual(thing2.other.name, "name1")


class TestSchemaSave(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_properties.clear()
        ontology.schema_models.clear()

    def test_schema_save_basic(self):
        class Thing(Schema):
            name = TextProperty()
        thing = Thing(name="name1")
        json_data = {}
        thing.dump(json_data)
        self.assertEqual(json_data["name"], "name1")
        self.assertEqual(json_data["instance_of"], "Thing")
        json_data2 = thing.dump()
        self.assertEqual(json_data2["name"], "name1")
        self.assertEqual(json_data2["instance_of"], "Thing")

    def test_schema_save_custom_property_name(self):
        class Thing(Schema):
            name = TextProperty(property_name="custom_name")
        thing = Thing(name="name1")
        json_data2 = thing.dump()
        self.assertEqual(json_data2["custom_name"], "name1")
        self.assertEqual(json_data2["instance_of"], "Thing")


# TODO: Schemas with property_name different than attrib name does not laod and save correclty