import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField,
                              RelationField)


class TestSchemaLoad(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_fields.clear()
        ontology.schema_models.clear()

    def test_schema_load_basic(self):
        class Thing(Schema):
            name = TextField()
        thing = Thing()
        json_data = {"instance_of": "Thing", "name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")

    def test_schema_load_instance_in_string(self):
        class Thing(Schema):
            name = TextField()
        thing = Thing()
        json_data = {"instance_of": "Thing", "name": "instance_of"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "instance_of")

    def test_schema_load_custom_field_name(self):
        class Thing(Schema):
            name = TextField(field_name="custom_name")
        thing = Thing()
        json_data = {"instance_of": "Thing", "custom_name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")

    def test_schema_load_schema_link(self):
        class Thing(Schema):  # NOSONAR
            name = TextField()

        class Thing2(Schema):
            other = RelationField("Thing")
        thing2 = Thing2()
        json_data = {"instance_of": "Thing2", "other": {"instance_of": "Thing", "name": "name1"}}
        self.assertIsNone(thing2.other)
        thing2.load(json_data)
        self.assertIsNotNone(thing2.other)
        self.assertEqual(thing2.other.name, "name1")


class TestSchemaSave(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_fields.clear()
        ontology.schema_models.clear()

    def test_schema_save_basic(self):
        class Thing(Schema):
            name = TextField()
        thing = Thing(name="name1")
        json_data = {}
        thing.save(json_data)
        self.assertEqual(json_data["name"], "name1")
        self.assertEqual(json_data["instance_of"], "Thing")
        json_data2 = thing.save()
        self.assertEqual(json_data2["name"], "name1")
        self.assertEqual(json_data2["instance_of"], "Thing")

    def test_schema_save_custom_field_name(self):
        class Thing(Schema):
            name = TextField(field_name="custom_name")
        thing = Thing(name="name1")
        json_data2 = thing.save()
        self.assertEqual(json_data2["custom_name"], "name1")
        self.assertEqual(json_data2["instance_of"], "Thing")


# TODO: Schemas with field_name different than attrib name does not laod and save correclty