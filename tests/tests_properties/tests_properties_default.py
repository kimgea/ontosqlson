import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)


class TestPropertiesDefault(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_properties.clear()
        ontology.schema_models.clear()

    def test_properties_text(self):
        class Thing(Schema):
            name = TextProperty(default="default")
        thing = Thing()
        self.assertEqual(thing.name, "default")
        thing.name = "name1"
        self.assertEqual(thing.name, "name1")

    def test_properties_integer(self):
        class Thing(Schema):
            name = IntegerProperty(default=1)
        thing = Thing()
        self.assertEqual(thing.name, 1)
        thing.name = 2
        self.assertEqual(thing.name, 2)

    def test_properties_positive_integer(self):
        class Thing(Schema):
            name = PositiveIntegerProperty(default=1)
        thing = Thing()
        self.assertEqual(thing.name, 1)
        thing.name = 2
        self.assertEqual(thing.name, 2)

    def test_properties_class(self):
        class Thing(Schema):
            name = TextProperty(default="default")
        class Thing2(Schema):
            other = ClassProperty("Thing",default=Thing(name="name1"))
        thing2 = Thing2()
        self.assertEqual(thing2.other.name, "name1")
        thing2.other.name = "new_name"
        self.assertEqual(thing2.other.name, "new_name")

    def test_properties_mix(self):
        class Thing(Schema):
            name = TextProperty(default="default")
        class Thing2(Schema):
            name2 = TextProperty(default="default2")
        class Thing3(Schema):
            other = ClassPropertyMix(["Thing", "Thing2"],default=Thing(name="name1"))
        thing3 = Thing3()
        self.assertEqual(thing3.other.name, "name1")
        thing3.other.name = "new_name"
        self.assertEqual(thing3.other.name, "new_name")

