import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField,
                              IntegerField)


# TODO: schema should not be alowed to have a field that already exist in one of its ancestors


class TestSchemaInheritance(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_fields.clear()
        ontology.schema_models.clear()

    def test_schema_inheritance_basic(self):
        class NameThing(Schema):
            name = TextField()

        class NumberThing(NameThing):
            number = IntegerField()

        name_thing = NameThing()
        number_thing = NumberThing()

        self.assertIsNone(name_thing.name)
        name_thing.name = "name1"

        self.assertEqual(name_thing.name, "name1")

        self.assertIsNone(number_thing.name)
        self.assertIsNone(number_thing.number)
        number_thing.name = "name2"
        number_thing.number = 2

        self.assertEqual(number_thing.name, "name2")
        self.assertEqual(number_thing.number, 2)
        self.assertEqual(name_thing.name, "name1")


    def test_schema_inheritance_init_subclass(self):
        class NameThing(Schema):
            name = TextField()
            _registry = dict()

            def __init_subclass__(cls, reg_name=None, **kwargs):
                super().__init_subclass__(**kwargs)
                if reg_name is not None:
                    cls._registry[reg_name] = cls

        class NumberThing(NameThing, reg_name="test"):
            number = IntegerField()

        class NumberThing2(NameThing):
            number2 = IntegerField()

        name_thing = NameThing(name="name_1")
        number_thing = NumberThing(name="name_2", number=2)
        number_thing2 = NumberThing2(name="name_3", number2=3)

        self.assertEqual(name_thing.name, "name_1")

        self.assertEqual(number_thing.name, "name_2")
        self.assertEqual(number_thing.number, 2)

        self.assertEqual(number_thing2.name, "name_3")
        self.assertEqual(number_thing2.number2, 3)

        self.assertEqual(len(name_thing._registry), 1)


    def test_schema_inheritance_mixin(self):
        class MixIn:
            def is_adult(self):
                return self.age >= 18

        class NameThing(Schema):
            name = TextField()

        class Person(MixIn, NameThing, Schema):
            age = IntegerField()

        person = Person(age=30)
        person2 = Person(age=15)

        self.assertTrue(person.is_adult())
        self.assertFalse(person2.is_adult())

        self.assertEqual(len(person._meta.parents), 1)



