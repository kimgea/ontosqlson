from ontosqlson.ontology import Ontology
from ontosqlson.field import (TextField,
                              IntegerField,
                              RelationField,
                              MixField)


def init_fields():

    ontology = Ontology()

    ontology.register_schema_fields("name", TextField())
    TextField(field_name="identifications", many=True)
    TextField(field_name="identifications", many=True)
    year_field = IntegerField(field_name="year", default=1985)  # NOSONAR
    # PositiveIntegerField(field_name="age")
    TextField(field_name="series_description")
    RelationField("TVSeries", field_name="tv_series")
    tv_season = RelationField("TVSeason", field_name="tv_season")  # NOSONAR
    MixField(["TVSeries", "TVSeason"], field_name="test")