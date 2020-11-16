import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField,
                              PositiveIntegerField,
                              RelationField)
from ontosqlson.field.field_types import (RelationFieldType)


class TestFieldPositiveInteger(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_fields.clear()
        ontology.schema_models.clear()

    def test_field_positive_integer(self):
        class Thing(Schema):
            name = PositiveIntegerField()

        thing = Thing(name=1)
        self.assertEqual(thing.name, 1)
        with self.assertRaises(ValueError):
            thing.name = -1
        self.assertEqual(thing.name, 1)

    def test_field_positive_integer_fix_it(self):
        class Thing(Schema):
            name = PositiveIntegerField(fix_value=True)

        thing = Thing(name=1)
        self.assertEqual(thing.name, 1)
        thing.name = -1
        self.assertEqual(thing.name, 0)
