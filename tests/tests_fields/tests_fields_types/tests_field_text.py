import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField,
                              PositiveIntegerField,
                              RelationField)
from ontosqlson.field.types import (RelationFieldType)


class TestFieldText(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_fields.clear()
        ontology.schema_models.clear()

    def test_field_class(self):
        class Thing(Schema):
            name = TextField(max_length=5)

        thing = Thing(name="thing")
        self.assertEqual(thing.name, "thing")
        with self.assertRaises(ValueError):
            thing.name = "to long text string, in valid"
        self.assertEqual(thing.name, "thing")