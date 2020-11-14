import unittest
from ontosqlson.ontology import Ontology
from ontosqlson.schema import Schema
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)


class TestSchemaMetaSettings(unittest.TestCase):
    def setUp(self):
        ontology = Ontology()
        ontology.schema_properties.clear()
        ontology.schema_models.clear()

    def test_schema_class_name_custom(self):
        class Thing(Schema):
            name = TextProperty()
            class Meta:
                schema_class_name = "ThingOther"
        thing = Thing()
        json_data = {"instance_of": "ThingOther", "name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")
        json_data2 = thing.save()
        self.assertEqual(json_data2["name"], "name1")
        self.assertEqual(json_data2["instance_of"], "ThingOther")

    def test_schema_object_name(self):
        class Thing(Schema):
            name = TextProperty()
            class Meta:
                schema_class_name = "ThingOther"
        thing = Thing(name="test")
        self.assertEqual(thing._meta.object_name, "Thing")
        self.assertEqual(thing._meta.schema_class_name, "ThingOther")

    def test_meta_schema_class_name_inheritance(self):
        class NameThing(Schema):
            name = TextProperty()

            class Meta:
                schema_class_name = "ThingOther2"

        class NumberThing(NameThing):
            number = IntegerProperty()

        class NumberThing2(NumberThing):
            number2 = IntegerProperty()

            class Meta:
                schema_class_name = "ThingOther"

        name_thing = NameThing(name="name_1")
        number_thing = NumberThing(name="name_2", number=2)
        number_thing2 = NumberThing2(name="name_3", number2=3)

        self.assertEqual(name_thing._meta.schema_class_name, "ThingOther2")
        self.assertEqual(number_thing._meta.schema_class_name, "NumberThing")
        self.assertEqual(number_thing2._meta.schema_class_name, "ThingOther")


    def test_instance_of_field_name_custom(self):
        class Thing(Schema):
            name = TextProperty()
            class Meta:
                instance_of_field_name = "is_type"
        thing = Thing()
        json_data = {"is_type": "Thing", "name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")
        json_data2 = thing.save()
        self.assertEqual(json_data2["name"], "name1")
        self.assertEqual(json_data2["is_type"], "Thing")

    def test_meta_parents_count(self):
        class NameThing(Schema):
            name = TextProperty()

        class NumberThing(NameThing):
            number = IntegerProperty()

        class NumberThing2(NumberThing):
            number2 = IntegerProperty()

        class NameThing2(Schema):
            name = TextProperty()

        class NumberThing3(NameThing2, NumberThing2):
            number2 = IntegerProperty()

        name_thing = NameThing(name="name_1")
        number_thing = NumberThing(name="name_2", number=2)
        number_thing2 = NumberThing2(name="name_3", number2=3)
        number_thing3 = NumberThing3(name="name_4", number2=4)

        self.assertEqual(len(name_thing._meta.parents), 0)
        self.assertEqual(len(number_thing._meta.parents), 1)
        self.assertEqual(len(number_thing2._meta.parents), 1)
        self.assertEqual(len(number_thing3._meta.parents), 2)

    def test_meta_ascendants_count(self):
        class NameThing(Schema):
            name = TextProperty()

        class NumberThing(NameThing):
            number = IntegerProperty()

        class NumberThing2(NumberThing):
            number2 = IntegerProperty()

        name_thing = NameThing(name="name_1")
        number_thing = NumberThing(name="name_2", number=2)
        number_thing2 = NumberThing2(name="name_3", number2=3)

        self.assertEqual(len(name_thing._meta.ascendants), 0)
        self.assertEqual(len(number_thing._meta.ascendants), 1)
        self.assertEqual(len(number_thing2._meta.ascendants), 2)

    def test_meta_concrete_model(self):
        class NameThing(Schema):
            name = TextProperty()

        class NumberThing(NameThing):
            number = IntegerProperty()

        class NumberThing2(NumberThing):
            number2 = IntegerProperty()

        name_thing = NameThing(name="name_1")
        number_thing = NumberThing(name="name_2", number=2)
        number_thing2 = NumberThing2(name="name_3", number2=3)

        self.assertEqual(name_thing._meta.concrete_model, NameThing)
        self.assertEqual(number_thing._meta.concrete_model, NumberThing)
        self.assertEqual(number_thing._meta.parents["NameThing"]()
                         ._meta.concrete_model, NameThing)
        self.assertEqual(number_thing2._meta.concrete_model, NumberThing2)
        self.assertEqual(number_thing2._meta.parents["NumberThing"]()
                         ._meta.concrete_model, NumberThing)
        self.assertEqual(number_thing2._meta.parents["NumberThing"]()
                         ._meta.parents["NameThing"]()
                         ._meta.concrete_model, NameThing)
