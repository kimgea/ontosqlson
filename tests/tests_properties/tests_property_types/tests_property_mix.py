import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)


class TestPropertyMix(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_properties.clear()
        ontology.schema_models.clear()

    def test_properties_mix_with_string(self):
        class Other(Schema):
            name = TextProperty()

            class Meta:
                schema_class_name = "OtherSpecial"
                instance_of_field_name = "is_type"

        class Thing(Schema):
            name = TextProperty()
            other = ClassPropertyMix([Other,])

        thing = Thing(other=Other(name="other"), name="thing")
        self.assertEqual(thing.name, "thing")
        self.assertEqual(thing.other.name, "other")
        self.assertEqual(thing.other._meta.instance_of_field_name, "is_type")
        self.assertEqual(thing.other._meta.schema_class_name, "OtherSpecial")
        thing.other = Other(name="new_other")
        self.assertEqual(thing.name, "thing")
        self.assertEqual(thing.other.name, "new_other")

        json_data = thing.save()

        self.assertEqual(json_data["name"], "thing")
        self.assertEqual(json_data["instance_of"], "Thing")
        self.assertEqual(json_data["other"]["name"], "new_other")
        self.assertEqual(json_data["other"]["is_type"], "OtherSpecial")