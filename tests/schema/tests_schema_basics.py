import unittest
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField)
import tests.setup.schemas as schema_models


class TestSchemaBasics(unittest.TestCase):

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
