from tests.setup.schemas import *



work = CreativeWork(name="fffff")

json_data = {
    "instance_of": "TVSeason",
    "name": "Season 1",
    "age": 1,
    "tv_series_custom_name": {
        "instance_of": "TVSeries",
        "name": "Dexter",
        "age": 22,
        "not_mapped_two": "should not be changed"
    },
    "not_mapped_one": "should not be changed"
}

print(json_data)
series1 = TVSeason()
print(series1.name)
print(series1.age)
print(series1.year)
print("---PRE_LOAD----")
series1.load(json_data)
print("---POST_LOAD----")
print(series1.name)
print(series1.age)
print(series1.year)
print(series1.tv_series_custom_name.name)
print(series1.tv_series_custom_name.age)
print(series1.tv_series_custom_name.series_description)
series1.tv_series_custom_name.name = "changed name"
series1.extra_variable = "Test new field added ynamically"
series1.identifications.append("id_1")
series1.identifications.append("id_2")
print(json_data)
print("---PRE_SAVE----")
series1.dump(data=json_data)
print("---POST_SAVE----")
print(json_data)
print("---------------------------------------")

"""
work = CreativeWork(name="fffff")

print(work)

tv = TVSeries()
print(tv._meta.object_name)


tv2 = TVSeries()
print(tv._meta.schema_class_name)

print("---------------------------------------")
print(tv)
print(tv2)
tv.name = "a"
print(tv)
print(tv2)
tv.name = "b"
tv2.name = "c"
print(tv)
print(tv2)
print("---------------------------------------")




tv_season = TVSeason(tv_series=tv, name="1")
tv_season2 = TVSeason(tv_series=tv2, name="2")
tv_episode = TVEpisode()
tv_episode.tv_season = tv_season
tv_episode.tv_series = tv
tv_episode.test = tv
tv_episode.test = tv_season
# tv_episode.test = tv_episode
print(tv_season, tv_season.tv_series)
print(tv_season2, tv_season2.tv_series)"""

# TODO: SOme refactoring.... clean up

# TODO: Import from list of diferent types

# TODO: instance_of... improve it? how?

"""
    # TODO: Field extentions
    - required
    - load_only
    - dump_only
    - allow_null
    
    - ontology
        - How to handle fields used on multile domains
            - Keep a sperate property set that is sent in to schema property?
        - label
        - comment
        -sub_property_of
    
"""

# TODO: Put invalid data (data in maped fields that are invalid) in invalid structure. Append __invalid, or seperate _invalid = {} field?

# TODO: Validate ClassProperty and ClassPropertyMix. Validate class on init, but string class name must validate later... or do runtime on add??? Skip checking if class exist?

# TODO: Make sure field does not have same name as one from an ascendant.... why?

# TODO: Versioning?

# TODO: Map to sql db. All in json column. But some shoud be posible to map other palces. Relations, and so on....  Use field and schema arguments, source????

# TODO: Support multiple ontologies?