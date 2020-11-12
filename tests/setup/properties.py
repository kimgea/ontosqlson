from ontosqlson.ontology import Ontology
from ontosqlson.properties import (TextProperty,
                                   IntegerProperty,
                                   PositiveIntegerProperty,
                                   ClassProperty,
                                   ClassPropertyMix)


def init_properties():

    ontology = Ontology()

    ontology.register_schema_property("name", TextProperty())
    TextProperty(property_name="identifications", many=True)
    TextProperty(property_name="identifications", many=True)
    year_property = IntegerProperty(property_name="year", default=1985)
    # PositiveIntegerProperty(property_name="age")
    TextProperty(property_name="series_description")
    ClassProperty("TVSeries", property_name="tv_series")
    tv_season = ClassProperty("TVSeason", property_name="tv_season")
    ClassPropertyMix(["TVSeries", "TVSeason"], property_name="test")