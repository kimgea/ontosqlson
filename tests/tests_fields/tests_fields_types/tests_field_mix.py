import unittest
from entschema.schema import Schema
from entschema.field import (TextField,
                             MixField)
from entschema.field.field_types import (TextFieldType)


class TestFieldMix(unittest.TestCase):

    def test_field_mix_with_string(self):
        class Other(Schema):
            name = TextField()

            class Meta:
                schema_class_name = "OtherSpecial"
                instance_of_field_name = "is_type"

        class Thing(Schema):
            other = MixField([Other, TextFieldType()])

        thing = Thing(other=Other(name="other"), name="thing")
        self.assertEqual(thing.name, "thing")
        self.assertEqual(thing.other.name, "other")
        self.assertEqual(thing.other._meta.instance_of_field_name, "is_type")
        self.assertEqual(thing.other._meta.schema_class_name, "OtherSpecial")
        thing.other = "test string"
        self.assertEqual(thing.name, "thing")
        self.assertEqual(thing.other, "test string")

        json_data = thing.save()

        self.assertEqual(json_data["instance_of"], "Thing")
        self.assertEqual(json_data["other"], "test string")