from ontosqlson.ontology import Ontology
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)
from ontosqlson.schema import Schema

from .properties import init_properties


init_properties()

ontology = Ontology()


# Duplicate from setup.properties
year_property = IntegerProperty(property_name="year", default=1985)
tv_season = ClassProperty("TVSeason", property_name="tv_season")


class Thing(Schema):
    name = TextProperty(property_name="name")  # exist when creating new
    identifications = ontology.schema_properties["identifications"]  # get existing

    class Meta:
        schema_class_name = "Thing"

    def __str__(self):
        return str(self.name)


class CreativeWork(Thing):
    year = year_property  # Use existing loaded in variable
    age = PositiveIntegerProperty(property_name="age")  # new not existing with custom name


class TVSeries(CreativeWork):
    series_description = TextProperty()  # new none existing without custom name. use attrib name


class TVSeason(CreativeWork):
    tv_series_custom_name = ClassProperty("TVSeries", property_name="tv_series")  # TODO: Not loading corectly, or dumping. Uses tv_series_custom_name instead of tv_series


class TVEpisode(CreativeWork):
    tv_series = ontology.schema_properties["tv_series"]
    tv_season = tv_season
    test = ontology.schema_properties["test"]
