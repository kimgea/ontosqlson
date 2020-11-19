import unittest
from entschema.schema import Schema
from entschema.field import (TextField,
                             PositiveIntegerField,
                             RelationField)
from entschema.field.field_types import (RelationFieldType)


class TestFieldPositiveInteger(unittest.TestCase):

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
