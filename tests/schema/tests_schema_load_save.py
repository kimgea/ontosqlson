import unittest
import copy
from entschema.schema import Schema
from entschema.field import (TextField,
                             RelationField)


json_import1 = dict(
                id="Q56876444",
                instance_of="TVShow",
                url="https://www.wikidata.org/wiki/Q56876444",
                title="The Mandalorian1",
                genre=[
                    dict(title="science fiction television", url="https://www.wikidata.org/wiki/Q336059", id="Q336059", instance_of="Genre"),
                    dict(title="Space Western1", url="https://www.wikidata.org/wiki/Q4235011", id="Q4235011", instance_of="Genre")
                ],
                creator=
                    dict(title="Jon Favreau", url="https://www.wikidata.org/wiki/Q295964", id="Q295964", instance_of="Creator")
                ,
                other_titles=["title1"]
            )


json_import2 = dict(
                id="Q56876444",
                instance_of="TVShow",
                url="https://www.wikidata.org/wiki/Q56876444",
                title="The Mandalorian",
                genre=[
                    dict(title="Space Western", url="https://www.wikidata.org/wiki/Q4235011", id="Q4235011", instance_of="Genre"),
                    dict(title="adventure film", url="https://www.wikidata.org/wiki/Q319221", id="Q319221", instance_of="Genre")
                ],
                creator=
                    dict(title="Changed", url="https://www.wikidata.org/wiki/Q295964", id="Q295964", instance_of="Creator")
                ,
                significant_event=[
                    dict(title="premier", url="https://www.wikidata.org/wiki/Q204854", id="Q204854", instance_of="SignificantEvent",
                         point_in_time="13 November 2019",
                         location=[dict(title="El Capitan Theatre", url="https://www.wikidata.org/wiki/Q849284", id="Q849284", instance_of="Location",)]
                         )
                ],
                other_titles=["title2", "title1"]
            )


class ThingBase(Schema):
    # id = TextField()
    url = TextField()
    title = TextField()


class Location(ThingBase):
    pass


class Genre(ThingBase):
    pass


class Creator(ThingBase):
   pass


class SignificantEvent(ThingBase):
    point_in_time = TextField()
    location = RelationField(Location, many=True)


class TVShow(ThingBase):
    genre = RelationField(Genre, many=True)
    significant_event = RelationField(SignificantEvent, many=True)
    creator = RelationField(Creator)
    other_titles = TextField(many=True)


class TestSchemaLoad(unittest.TestCase):

    def test_schema_load_basic(self):
        class Thing(Schema):
            name = TextField()
        thing = Thing()
        json_data = {"instance_of": "Thing", "name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")

    def test_schema_load_instance_in_string(self):
        class Thing(Schema):
            name = TextField()
        thing = Thing()
        json_data = {"instance_of": "Thing", "name": "instance_of"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "instance_of")

    def test_schema_load_custom_field_name(self):
        class Thing(Schema):
            name = TextField(field_name="custom_name")
        thing = Thing()
        json_data = {"instance_of": "Thing", "custom_name": "name1"}
        self.assertIsNone(thing.name)
        thing.load(json_data)
        self.assertEqual(thing.name, "name1")

    def test_schema_load_schema_link(self):
        class Thing(Schema):  # NOSONAR
            name = TextField()

        class Thing2(Schema):
            other = RelationField(Thing)
        thing2 = Thing2()
        json_data = {"instance_of": "Thing2", "other": {"instance_of": "Thing", "name": "name1"}}
        self.assertIsNone(thing2.other)
        thing2.load(json_data)
        self.assertIsNotNone(thing2.other)
        self.assertEqual(thing2.other.name, "name1")

    def test_schema_load_update(self):
        data1 = copy.deepcopy(json_import1)
        data2 = copy.deepcopy(json_import2)
        show = TVShow()
        show.load(data1)
        self.assertEqual(show.id, "Q56876444")
        self.assertEqual(show.url, "https://www.wikidata.org/wiki/Q56876444")
        self.assertEqual(show.title, "The Mandalorian1")

        self.assertEqual(len(show.other_titles), 1)
        self.assertEqual(show.other_titles[0], "title1")

        self.assertEqual(len(show.genre), 2)
        self.assertEqual(show.genre[0].id, "Q336059")
        self.assertEqual(show.genre[0].url, "https://www.wikidata.org/wiki/Q336059")
        self.assertEqual(show.genre[0].title, "science fiction television")
        self.assertEqual(show.genre[1].id, "Q4235011")
        self.assertEqual(show.genre[1].url, "https://www.wikidata.org/wiki/Q4235011")
        self.assertEqual(show.genre[1].title, "Space Western1")

        self.assertEqual(show.creator.id, "Q295964")
        self.assertEqual(show.creator.url, "https://www.wikidata.org/wiki/Q295964")
        self.assertEqual(show.creator.title, "Jon Favreau")

        show.load(data2)

        self.assertEqual(show.id, "Q56876444")
        self.assertEqual(show.url, "https://www.wikidata.org/wiki/Q56876444")
        self.assertEqual(show.title, "The Mandalorian")

        self.assertEqual(len(show.other_titles), 2)
        self.assertEqual(show.other_titles[0], "title1")
        self.assertEqual(show.other_titles[1], "title2")

        self.assertEqual(len(show.genre), 3)
        self.assertEqual(show.genre[0].id, "Q336059")
        self.assertEqual(show.genre[0].url, "https://www.wikidata.org/wiki/Q336059")
        self.assertEqual(show.genre[0].title, "science fiction television")
        self.assertEqual(show.genre[1].id, "Q4235011")
        self.assertEqual(show.genre[1].url, "https://www.wikidata.org/wiki/Q4235011")
        self.assertEqual(show.genre[1].title, "Space Western")
        self.assertEqual(show.genre[2].id, "Q319221")
        self.assertEqual(show.genre[2].url, "https://www.wikidata.org/wiki/Q319221")
        self.assertEqual(show.genre[2].title, "adventure film")

        self.assertEqual(show.creator.id, "Q295964")
        self.assertEqual(show.creator.url, "https://www.wikidata.org/wiki/Q295964")
        self.assertEqual(show.creator.title, "Changed")

        self.assertEqual(show.significant_event[0].id, "Q204854")
        self.assertEqual(show.significant_event[0].url, "https://www.wikidata.org/wiki/Q204854")
        self.assertEqual(show.significant_event[0].title, "premier")
        self.assertEqual(show.significant_event[0].point_in_time, "13 November 2019")
        self.assertEqual(show.significant_event[0].location[0].id, "Q849284")
        self.assertEqual(show.significant_event[0].location[0].url, "https://www.wikidata.org/wiki/Q849284")
        self.assertEqual(show.significant_event[0].location[0].title, "El Capitan Theatre")

        del show.genre[0]
        self.assertEqual(len(show.genre), 2)
        show.other_titles.append("title3")
        self.assertEqual(len(show.other_titles), 3)
        show.title = "new title"
        self.assertEqual(show.title, "new title")


class TestSchemaSave(unittest.TestCase):

    def test_schema_save_basic(self):
        class Thing(Schema):
            name = TextField()
        thing = Thing(name="name1")
        json_data = {}
        thing.save(json_data)
        self.assertEqual(json_data["name"], "name1")
        self.assertEqual(json_data["instance_of"], "Thing")
        json_data2 = thing.save()
        self.assertEqual(json_data2["name"], "name1")
        self.assertEqual(json_data2["instance_of"], "Thing")

    def test_schema_save_custom_field_name(self):
        class Thing(Schema):
            name = TextField(field_name="custom_name")
        thing = Thing(name="name1")
        json_data2 = thing.save()
        self.assertEqual(json_data2["custom_name"], "name1")
        self.assertEqual(json_data2["instance_of"], "Thing")

    def test_schema_save_slightly_more_complex(self):
        data1 = copy.deepcopy(json_import1)
        show = TVShow()
        show.load(data1)
        data2 = show.save()

        self.assertEqual(data2["id"], "Q56876444")
        self.assertEqual(data2["url"], "https://www.wikidata.org/wiki/Q56876444")
        self.assertEqual(data2["title"], "The Mandalorian1")

        self.assertEqual(len(data2["other_titles"]), 1)
        self.assertEqual(data2["other_titles"][0], "title1")

        self.assertEqual(len(data2["genre"]), 2)
        self.assertEqual(data2["genre"][0]["id"], "Q336059")
        self.assertEqual(data2["genre"][0]["url"], "https://www.wikidata.org/wiki/Q336059")
        self.assertEqual(data2["genre"][0]["title"], "science fiction television")
        self.assertEqual(data2["genre"][1]["id"], "Q4235011")
        self.assertEqual(data2["genre"][1]["url"], "https://www.wikidata.org/wiki/Q4235011")
        self.assertEqual(data2["genre"][1]["title"], "Space Western1")

        self.assertEqual(data2["creator"]["id"], "Q295964")
        self.assertEqual(data2["creator"]["url"], "https://www.wikidata.org/wiki/Q295964")
        self.assertEqual(data2["creator"]["title"], "Jon Favreau")
