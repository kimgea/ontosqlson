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
year_field = ontology.schema_fields["year"]
tv_season = ontology.schema_fields["tv_season"]


class Thing(Schema):
    name = ontology.schema_fields["name"]
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
    tv_series_custom_name = ontology.schema_fields["tv_series"]


class TVEpisode(CreativeWork):
    tv_series = ontology.schema_fields["tv_series"]
    tv_season = tv_season
    test = ontology.schema_fields["test"]
