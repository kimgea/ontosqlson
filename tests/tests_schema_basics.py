import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField)
import tests.setup.schemas as schema_models


# TODO: schema should not be alowed to have a field that already exist in one of its ancestors


class TestSchemaBasics(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_fields.clear()
        ontology.schema_models.clear()

    def test_schema_basics_module(self):
        class Thing2(Schema):
            name = TextField()
        thing = Thing2(name="n")
        self.assertEqual(thing.__module__, __name__)

    def test_schema_basics_inheritance_module(self):
        class Thing2(schema_models.CreativeWork):
            name = TextField()
        thing = Thing2(name="n")
        self.assertEqual(thing.__module__, __name__)

    def test_schema_basics_extra_var(self):
        class Thing2(Schema):
            name = TextField()

        thing = Thing2(name="n", extra=1)
        self.assertEqual(thing.name, "n")
        self.assertEqual(thing.extra, 1)
        json_data = thing.save()
        self.assertTrue("name" in json_data)
        self.assertTrue("extra" not in json_data)
