import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)


class TestPropertyRegistration(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_properties.clear()
        ontology.schema_models.clear()

    def test_loose_property_is_registered(self):
        TextProperty(property_name="identifications", many=True)
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_property_duplication_register_same(self):
        TextProperty(property_name="identifications", many=True)
        TextProperty(property_name="identifications", many=True)
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_property_duplication_register_different(self):
        TextProperty(property_name="identifications", many=True)
        with self.assertRaises(ValueError):
            TextProperty(property_name="identifications", many=False)
        ontology = Ontology()
        self.assertTrue("identifications" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_class_property(self):
        class Thing(Schema):
            name = TextProperty()
        ontology = Ontology()
        thing = Thing()  # NOSONAR
        self.assertTrue("name" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_class_property_exist(self):
        TextProperty(property_name="name")
        class Thing(Schema):
            name = TextProperty()
        ontology = Ontology()
        thing = Thing()  # NOSONAR
        self.assertTrue("name" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_class_property_custom_name(self):
        class Thing(Schema):
            name = TextProperty(property_name="name_custom")
        ontology = Ontology()
        thing = Thing()  # NOSONAR
        self.assertFalse("name" in ontology.schema_properties)
        self.assertTrue("name_custom" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_class_property_duplicate(self):
        class Thing(Schema):
            name = TextProperty()

        class Thing2(Schema):
            name = TextProperty()
        ontology = Ontology()
        thing = Thing()  # NOSONAR
        thing2 = Thing2()  # NOSONAR
        self.assertFalse("name_other" in ontology.schema_properties)
        self.assertTrue("name" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_class_property_duplicate_custom_name(self):
        class Thing(Schema):
            name = TextProperty(property_name="name_custom")

        class Thing2(Schema):
            name = TextProperty(property_name="name_custom")

        ontology = Ontology()
        thing = Thing()  # NOSONAR
        thing2 = Thing2()  # NOSONAR
        self.assertFalse("name" in ontology.schema_properties)
        self.assertFalse("name_other" in ontology.schema_properties)
        self.assertTrue("name_custom" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_class_property_from_ontology_property_list(self):
        TextProperty(property_name="name")
        ontology = Ontology()

        class Thing(Schema):
            name = ontology.schema_properties["name"]
        thing = Thing()  # NOSONAR
        self.assertTrue("name" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_class_property_from_variable(self):
        name_property = TextProperty(property_name="name")

        class Thing(Schema):
            name = name_property

        thing = Thing()  # NOSONAR
        ontology = Ontology()
        self.assertTrue("name" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)

    def test_class_property_messy(self):
        TextProperty(property_name="name")
        name_one_property = TextProperty(property_name="name")
        ontology = Ontology()
        ontology.register_schema_property("number_positive", PositiveIntegerProperty())
        PositiveIntegerProperty(property_name="number_positive")

        class Thing(Schema):
            name_one = name_one_property
            name_two = TextProperty(property_name="name_two")
            name_three = TextProperty(property_name="name_custom")
            number = IntegerProperty()
            number_two = IntegerProperty(property_name="number_custom")
            number_positive = PositiveIntegerProperty()

        ontology.register_schema_property("mix_one", ClassProperty(Thing))

        class Thing2(Schema):
            name_one = name_one_property
            name_two = TextProperty(property_name="name_two")
            name_three = TextProperty(property_name="name_custom")
            number = IntegerProperty()
            number_two = IntegerProperty(property_name="number_custom")
            number_positive = PositiveIntegerProperty()
            mix_one = ClassProperty(Thing)

        class Thing3(Schema):
            mix_two = ClassPropertyMix([Thing, Thing2], property_name="mix_two_custom")

        thing = Thing()  # NOSONAR
        thing2 = Thing2()  # NOSONAR
        thing3 = Thing3()  # NOSONAR

        self.assertTrue("name" in ontology.schema_properties)
        self.assertTrue("name_two" in ontology.schema_properties)
        self.assertTrue("name_custom" in ontology.schema_properties)
        self.assertTrue("number" in ontology.schema_properties)
        self.assertTrue("number_custom" in ontology.schema_properties)
        self.assertTrue("number_positive" in ontology.schema_properties)
        self.assertTrue("mix_one" in ontology.schema_properties)
        self.assertTrue("mix_two_custom" in ontology.schema_properties)

        self.assertFalse("name_one" in ontology.schema_properties)
        self.assertFalse("name_three" in ontology.schema_properties)
        self.assertFalse("number_two" in ontology.schema_properties)
        self.assertFalse("mix_two" in ontology.schema_properties)

        self.assertEqual(len(ontology.schema_properties), 8)

    """def test_class_property_duplicate_same_class_not_allowed(self):
        # TODO: move to class tests.... not a registration issue?
        class Thing(Schema):
            name = TextProperty(property_name="name_custom")
            name_two = TextProperty(property_name="name_custom")

        ontology = SchemaCollection()
        with self.assertRaises(ValueError):
            thing = Thing()
        self.assertFalse("name" in ontology.schema_properties)
        self.assertFalse("name_other" in ontology.schema_properties)
        self.assertTrue("name_custom" in ontology.schema_properties)
        self.assertEqual(len(ontology.schema_properties), 1)"""