from ontosqlson.ontology import Ontology
from ontosqlson.field import (TextField,
                              IntegerField,
                              PositiveIntegerField,
                              RelationField)
from ontosqlson.schema import Schema

from .schema_fields import init_fields


init_fields()

ontology = Ontology()


# Duplicate from setup.field
year_field = IntegerField(field_name="year", default=1985)
tv_season = RelationField("TVSeason", field_name="tv_season")


class Thing(Schema):
    name = TextField(field_name="name")  # exist when creating new
    identifications = ontology.schema_fields["identifications"]  # get existing

    class Meta:
        schema_class_name = "Thing"

    def __str__(self):
        return str(self.name)


class CreativeWork(Thing):
    year = year_field  # Use existing loaded in variable
    age = PositiveIntegerField(field_name="age")  # new not existing with custom name


class TVSeries(CreativeWork):
    series_description = TextField()  # new none existing without custom name. use attrib name


class TVSeason(CreativeWork):
    tv_series_custom_name = RelationField("TVSeries", field_name="tv_series")  # TODO: Not loading corectly, or dumping. Uses tv_series_custom_name instead of tv_series


class TVEpisode(CreativeWork):
    tv_series = ontology.schema_fields["tv_series"]
    tv_season = tv_season
    test = ontology.schema_fields["test"]
