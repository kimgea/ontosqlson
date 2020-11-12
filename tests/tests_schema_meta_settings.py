import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)


class TestSchemaMetaSettings(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_properties.clear()
        ontology.schema_models.clear()

    def test_schema_class_name_custom(self):
        class Thing(Schema):
            name = TextProperty()
            class Meta:
                schema_class_name = "ThingOther"
        thing = Thing()
        json_data = {"instance_of": "ThingOther", "name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")
        json_data2 = thing.dump()
        self.assertEqual(json_data2["name"], "name1")
        self.assertEqual(json_data2["instance_of"], "ThingOther")

    def test_instance_of_field_name_custom(self):
        class Thing(Schema):
            name = TextProperty()
            class Meta:
                instance_of_field_name = "is_type"
        thing = Thing()
        json_data = {"is_type": "Thing", "name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")
        json_data2 = thing.dump()
        self.assertEqual(json_data2["name"], "name1")
        self.assertEqual(json_data2["is_type"], "Thing")