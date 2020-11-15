import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField,
                              PositiveIntegerField,
                              RelationField)
from ontosqlson.field.types import (RelationFieldType)


class TestFieldClass(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_fields.clear()
        ontology.schema_models.clear()

    def test_field_class(self):
        class Other(Schema):
            name = TextField()

            class Meta:
                schema_class_name = "OtherSpecial"
                instance_of_field_name = "is_type"

        class Thing(Schema):
            name = TextField()
            other = RelationField(Other)
            other2 = RelationField(RelationFieldType(Other))
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

    def test_field_class_inheritance(self):
        class Other(Schema):
            name = TextField()

        class Thing(Other):
            age = PositiveIntegerField()

            class Meta:
                schema_class_name = "OtherSpecial"
                instance_of_field_name = "is_type"

        class Work(Schema):
            name = TextField()
            thing = RelationField("Other")

        work = Work(thing=Thing(name="other", age=22), name="work")
        self.assertEqual(work.name, "work")
        self.assertEqual(work.thing.name, "other")
        self.assertEqual(work.thing.age, 22)
        self.assertEqual(work.thing._meta.instance_of_field_name, "is_type")
        self.assertEqual(work.thing._meta.schema_class_name, "OtherSpecial")
        work.thing = Thing(name="new_other", age=33)
        self.assertEqual(work.name, "work")
        self.assertEqual(work.thing.name, "new_other")
        self.assertEqual(work.thing.age, 33)

        json_data = work.save()

        self.assertEqual(json_data["name"], "work")
        self.assertEqual(json_data["instance_of"], "Work")
        self.assertEqual(json_data["thing"]["name"], "new_other")
        self.assertEqual(json_data["thing"]["is_type"], "OtherSpecial")