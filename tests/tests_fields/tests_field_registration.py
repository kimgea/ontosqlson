import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField,
                              IntegerField,
                              PositiveIntegerField,
                              RelationField,
                              MixField)


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

    def test_class_field(self):
        class Thing(Schema):
            name = TextField()
        ontology = Ontology()
        thing = Thing()  # NOSONAR
        self.assertTrue("name" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_exist(self):
        TextField(field_name="name")
        class Thing(Schema):
            name = TextField()
        ontology = Ontology()
        thing = Thing()  # NOSONAR
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
        class Thing(Schema):
            name = TextField()

        class Thing2(Schema):
            name = TextField()
        ontology = Ontology()
        thing = Thing()  # NOSONAR
        thing2 = Thing2()  # NOSONAR
        self.assertFalse("name_other" in ontology.schema_fields)
        self.assertTrue("name" in ontology.schema_fields)
        self.assertEqual(len(ontology.schema_fields), 1)

    def test_class_field_duplicate_custom_name(self):
        class Thing(Schema):
            name = TextField(field_name="name_custom")

        class Thing2(Schema):
            name = TextField(field_name="name_custom")

        ontology = Ontology()
        thing = Thing()  # NOSONAR
        thing2 = Thing2()  # NOSONAR
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
        TextField(field_name="name")
        name_one_field = TextField(field_name="name")
        ontology = Ontology()
        ontology.register_schema_fields("number_positive", PositiveIntegerField())
        PositiveIntegerField(field_name="number_positive")

        class Thing(Schema):
            name_one = name_one_field
            name_two = TextField(field_name="name_two")
            name_three = TextField(field_name="name_custom")
            number = IntegerField()
            number_two = IntegerField(field_name="number_custom")
            number_positive = PositiveIntegerField()

        ontology.register_schema_fields("mix_one", RelationField(Thing))

        class Thing2(Schema):
            name_one = name_one_field
            name_two = TextField(field_name="name_two")
            name_three = TextField(field_name="name_custom")
            number = IntegerField()
            number_two = IntegerField(field_name="number_custom")
            number_positive = PositiveIntegerField()
            mix_one = RelationField(Thing)

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