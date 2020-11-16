import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField,
                              IntegerField,
                              PositiveIntegerField,
                              RelationField,
                              MixField)
from ontosqlson.field.validators import FieldValidatorBase


class TestFieldRegistration(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_fields.clear()
        ontology.schema_models.clear()

    def test_loose_field_is_registered(self):
        TextField(field_name="identifications", many=True)
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_field_duplication_register_same(self):
        TextField(field_name="identifications", many=True)
        with self.assertRaises(ValueError):
            TextField(field_name="identifications", many=True)
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_field_duplication_register_different(self):
        TextField(field_name="identifications", many=True)
        with self.assertRaises(ValueError):
            TextField(field_name="identifications", many=False)
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_field_duplication_register_different_validators(self):
        TextField(field_name="identifications", max_length=3)
        with self.assertRaises(ValueError):
            TextField(field_name="identifications", max_length=2)
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_field_duplication_register_same_validators(self):
        TextField(field_name="identifications", max_length=3)
        with self.assertRaises(ValueError):
            TextField(field_name="identifications", max_length=3)
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_field_duplication_register_different_custom_validators(self):
        class CustomValidator(FieldValidatorBase):
            def __init__(self, val=None):
                self.val = val
            def is_valid(self, value):
                return True

        TextField(field_name="identifications", validators=[CustomValidator(1)])
        with self.assertRaises(ValueError):
            TextField(field_name="identifications", validators=[CustomValidator(2)])
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_field_duplication_register_same_custom_validators(self):
        class CustomValidator(FieldValidatorBase):
            def __init__(self, val=None):
                self.val = val
            def is_valid(self, value):
                return True
        TextField(field_name="identifications", validators=[CustomValidator(1)])
        with self.assertRaises(ValueError):
            TextField(field_name="identifications", validators=[CustomValidator(1)])
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field(self):
        class Thing(Schema):
            name = TextField()
        ontology = Ontology()
        thing = Thing()  # NOSONAR
        self.assertTrue("name" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_exist(self):
        TextField(field_name="name")
        with self.assertRaises(ValueError):
            class Thing(Schema):
                name = TextField()
        ontology = Ontology()
        self.assertTrue("name" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_custom_name(self):
        class Thing(Schema):
            name = TextField(field_name="name_custom")
        ontology = Ontology()
        thing = Thing()  # NOSONAR
        self.assertFalse("name" in ontology.schema_fields)
        self.assertTrue("name_custom" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_duplicate(self):
        name_field = TextField()
        class Thing(Schema):
            name = TextField()

        with self.assertRaises(ValueError):
            class Thing2(Schema):
                name = TextField()
        ontology = Ontology()
        self.assertFalse("name_other" in ontology.schema_fields)
        self.assertTrue("name" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_duplicate_custom_name(self):
        class Thing(Schema):
            name = TextField(field_name="name_custom")

        with self.assertRaises(ValueError):
            class Thing2(Schema):
                name2 = TextField(field_name="name_custom")

        ontology = Ontology()
        self.assertFalse("name" in ontology.schema_fields)
        self.assertFalse("name_other" in ontology.schema_fields)
        self.assertTrue("name_custom" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_from_ontology_field_list(self):
        TextField(field_name="name")
        ontology = Ontology()

        class Thing(Schema):
            name = ontology.schema_fields["name"]
        thing = Thing()  # NOSONAR
        self.assertTrue("name" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_from_variable(self):
        name_field = TextField(field_name="name")

        class Thing(Schema):
            name = name_field

        thing = Thing()  # NOSONAR
        ontology = Ontology()
        self.assertTrue("name" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_messy(self):
        name_one_field = TextField(field_name="name")
        with self.assertRaises(ValueError):
            TextField(field_name="name")
        ontology = Ontology()
        ontology.register_schema_fields("number_positive", PositiveIntegerField())
        with self.assertRaises(ValueError):
            PositiveIntegerField(field_name="number_positive")

        class Thing(Schema):
            name_one = name_one_field
            name_two = TextField(field_name="name_two")
            name_three = TextField(field_name="name_custom")
            number = IntegerField()
            number_two = IntegerField(field_name="number_custom")
            number_positive = ontology.schema_fields["number_positive"]

        ontology.register_schema_fields("mix_one", RelationField(Thing))

        class Thing2(Schema):
            name_one = name_one_field
            name_two = ontology.schema_fields["name_two"]
            name_three = ontology.schema_fields["name_custom"]
            number = ontology.schema_fields["number"]
            number_two = ontology.schema_fields["number_custom"]
            number_positive = ontology.schema_fields["number_positive"]
            mix_one = ontology.schema_fields["mix_one"]

        class Thing3(Schema):
            mix_two = MixField([Thing, Thing2], field_name="mix_two_custom")

        thing = Thing()  # NOSONAR
        thing2 = Thing2()  # NOSONAR
        thing3 = Thing3()  # NOSONAR

        self.assertTrue("name" in ontology.schema_fields)
        self.assertTrue("name_two" in ontology.schema_fields)
        self.assertTrue("name_custom" in ontology.schema_fields)
        self.assertTrue("number" in ontology.schema_fields)
        self.assertTrue("number_custom" in ontology.schema_fields)
        self.assertTrue("number_positive" in ontology.schema_fields)
        self.assertTrue("mix_one" in ontology.schema_fields)
        self.assertTrue("mix_two_custom" in ontology.schema_fields)

        self.assertFalse("name_one" in ontology.schema_fields)
        self.assertFalse("name_three" in ontology.schema_fields)
        self.assertFalse("number_two" in ontology.schema_fields)
        self.assertFalse("mix_two" in ontology.schema_fields)

        self.assertEqual(len(ontology.schema_fields), 8)

    """def test_class_field_duplicate_same_class_not_allowed(self):
        # TODO: move to class tests.... not a registration issue?
        class Thing(Schema):
            name = TextField(field_name="name_custom")
            name_two = TextField(field_name="name_custom")

        ontology = SchemaCollection()
        with self.assertRaises(ValueError):
            thing = Thing()
        self.assertFalse("name" in ontology.schema_fields)
        self.assertFalse("name_other" in ontology.schema_fields)
        self.assertTrue("name_custom" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)"""