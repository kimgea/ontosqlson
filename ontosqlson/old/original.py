from itertools import chain
import inspect
from weakref import WeakKeyDictionary
import copy
from collections import OrderedDict, defaultdict
import sys
import threading


lock = threading.Lock()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SchemaCollection(metaclass=Singleton):
    def __init__(self):
        self.schema_models = {}
        self.schema_properties = {}

    def register_schema_model(self, schema_name, schema_model):
        self.schema_models[schema_name] = schema_model

    def register_schema_property(self, property_name, property_model):
        self.schema_properties[property_name] = property_model


########################################################################################################################


class Options:
    def __init__(self, meta, parents):
        self._meta = meta
        self._parents_holder = parents

        # self.local_fields = list()  # TODO: Nesesary to generate json ontology schemas. Can wait

        self.schema_class_name = None
        self.parents = OrderedDict()
        self.ascendants = dict()
        self.concrete_model = None

    def _get_ascendants(self):
        if not self.parents:
            return self.ascendants

        if self.ascendants:
            # Already processed
            return self.ascendants

        for parent_name in self.parents:
            parent = self.parents[parent_name]
            self.ascendants[parent._meta.object_name] = parent
            partent_ascendants = parent._meta._get_ascendants()
            if partent_ascendants:
                self.ascendants.update(partent_ascendants)

        return self.ascendants

    def contribute_to_class(self, cls, name):
        cls._meta = self
        self.model = cls

        # Default values
        self.object_name = cls.__name__
        self.schema_class_name = self.object_name
        self.schema_collection = SchemaCollection()

        if self._parents_holder:
            for parent in self._parents_holder:
                if not hasattr(parent, "_meta"):
                    continue
                self.parents[parent._meta.object_name] = parent
        del self._parents_holder

        self._get_ascendants()

        if self._meta:
            meta_attrs = self._meta.__dict__.copy()
            for name in self._meta.__dict__:
                if name.startswith('__'):
                    del meta_attrs[name]
            for attr_name in meta_attrs:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs[attr_name])
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self._meta, attr_name))
        del self._meta


def _has_contribute_to_class(value):
    return not inspect.isclass(value) and hasattr(value, 'contribute_to_class')


class SchemaBase(type):

    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__
        # Also ensure initialization is only performed for subclasses of Schema
        # (excluding Schema class itself).
        parents = [b for b in bases if isinstance(b, SchemaBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_attrs = {'__module__': module}
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell
        attr_meta = attrs.pop('Meta', None)

        contributable_attrs = {}
        for obj_name, obj in list(attrs.items()):
            if _has_contribute_to_class(obj):
                contributable_attrs[obj_name] = obj
            else:
                new_attrs[obj_name] = obj

        new_class = super_new(cls, name, bases, new_attrs, **kwargs)

        meta = attr_meta or getattr(new_class, 'Meta', None)
        new_class.add_to_class('_meta', Options(meta, parents))

        # Add remaining attributes (those with a contribute_to_class() method)
        # to the class.
        for obj_name, obj in contributable_attrs.items():
            new_class.add_to_class(obj_name, obj)

        new_class._meta.concrete_model = new_class
        new_class._meta.schema_collection.register_schema_model(
            new_class._meta.schema_class_name, new_class._meta.concrete_model)

        """def _include_attr(obj, attr):
            if attr != "name":
                return False
            print("_-_-_-_")
            print(attr)
            print(dir(obj.name))
            print(getattr(obj, attr))

            print(getattr(getattr(obj, attr), "__dict__"))
            print(getattr(getattr(obj, attr), "_is_schema_property"))
            if getattr(getattr(obj, attr), "_is_schema_property", False):
                return True
            return False
        # return set([attr for attr in dir(self) if _include_attr(attr)])
        # print(dir(new_class))
        print( set([attr for attr in dir(new_class) if _include_attr(new_class, attr)]))"""

        return new_class

    def test(cls):
        return "______ TEST ________"

    def add_to_class(cls, name, value):
        if _has_contribute_to_class(value):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class Schema(metaclass=SchemaBase):
    """
    Monkey patching is likely to fail
    """
    def __init__(self, **kwargs):
        fields = self._get_fields()

        self._schema_collection = SchemaCollection()

        if kwargs:
            for key in kwargs.keys():
                if key in fields:
                    setattr(self, key, kwargs[key])
        super().__init__()

    def load(self, data):
        instance_of = data["instance_of"]
        try:
            if instance_of != self._meta.schema_class_name:
                raise ValueError("Invalid Schema class: {schema_class_name} not in {instance_of}".format(
                    schema_class_name=self._meta.schema_class_name, instance_of=instance_of))
        except:
            if self._meta.schema_class_name not in instance_of:
                raise ValueError("Invalid Schema class: {schema_class_name} not in {instance_of}".format(
                    schema_class_name=self._meta.schema_class_name, instance_of=instance_of))

        fields = self._get_fields()
        for key in data.keys():
            if key in fields:
                value = data[key]
                try:
                    if "instance_of" in data[key]:
                        obj = self._meta.schema_collection.schema_models[data[key]["instance_of"]]()
                        obj.load(data[key])
                        value = obj
                except TypeError:
                    pass
                setattr(self, key, value)

    def dump(self, data=None):
        if data is None:
            data = dict()
        fields = self._get_fields(schema_field_only=True)
        for field in fields:
            if getattr(getattr(getattr(self, field), "_meta", {}), "schema_class_name", None) is not None:
                data[field] = getattr(self, field).dump(data[field])
            else:
                data[field] = getattr(self, field)
        return data

    def _get_fields(self, schema_field_only=False):
        def _include_attr(attr):
            if attr.startswith("__"):
                return False
            if callable(getattr(self, attr)):
                return False
            if schema_field_only:
                if getattr(getattr(self._meta.concrete_model, attr, {}), "_is_schema_property", False):
                    return True
                return False

            return True
        return set([attr[0] for attr in inspect.getmembers(self) if _include_attr(attr[0])])

    @classmethod
    def _prepare(cls):
        """Create some methods once self._meta has been populated."""
        opts = cls._meta
        opts._prepare(cls)

    def _is_schema_type(self, schema_type):
        if isinstance(schema_type, str):
            if self._meta.schema_class_name == schema_type:
                return True
            for ascendant in self._meta.ascendants.values():
                if ascendant._meta.schema_class_name == schema_type:
                    return True
            return False
        if self._meta.concrete_model == schema_type:
            return True
        for ascendant in self._meta.ascendants.values():
            if ascendant._meta.concrete_model == schema_type:
                return True
        return False


########################################################################################################################


class SchemaPropertyBase(object):
    def __init__(self, range_includes, default=None, many=False, *args, **kwargs):
        self._many = many
        self.default = default
        self.values = WeakKeyDictionary()
        self._is_schema_property = True
        self.range_includes = []
        self.range_includes_classes = []
        self.range_includes_class_names = []
        for i in range_includes:
            self.range_includes.append(i)
            if hasattr(i, "_meta"):
                self.range_includes_classes.append(i)
                self.range_includes_class_names.append(i._meta.schema_class_name)
            else:
                self.range_includes_class_names.append(i)

        self._validate_default_value()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._many:
            if instance not in self.values:
                self.values[instance] = []
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        if self._many:
            for val in value:
                self._validate_property_type(val)
        else:
            self._validate_property_type(value)
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]

    def _validate_default_value(self):
        if self.default is None:
            return
        self._validate_property_type(self.default)

    def _validate_property_type(self, value):
        if hasattr(value, "_meta"):
            for ok_range in self.range_includes_class_names:
                if value._is_schema_type(ok_range):
                    return

            raise ValueError("Invalid property type: {value} not in {range_includes}".format(
                value=value._meta.schema_class_name, range_includes=self.range_includes_class_names))

        if isinstance(value, str) and str in self.range_includes:
            return
        if isinstance(value, int) and int in self.range_includes:
            return

        raise ValueError("Invalid property type: {value} not in {range_includes}".format(
            value=type(value), range_includes=self.range_includes_class_names))


def domain_is_in_list(types, domain_list):
    for itr in domain_list:
        if itr in types:
            return True
    return False


class TextProperty(SchemaPropertyBase):
    def __init__(self, default=None, many=False, *args, **kwargs):
        super().__init__([str], default=default, many=many, *args, **kwargs)


class IntegerProperty(SchemaPropertyBase):
    def __init__(self, default=None, many=False, *args, **kwargs):
        super().__init__([int], default=default, many=many, *args, **kwargs)


class PositiveIntegerProperty(SchemaPropertyBase):
    def __init__(self, default=None, many=False, *args, **kwargs):
        super().__init__([int], default=default, many=many, *args, **kwargs)


class ClassProperty(SchemaPropertyBase):
    def __init__(self, range_type, default=None, many=False, *args, **kwargs):
        if not isinstance(range_type, str) and not hasattr(range_type, "_meta"):
            raise ValueError("Invalid range value: Must be a schema class or a string name of a schema class")
        super().__init__([range_type], default=default, many=many, *args, **kwargs)


class ClassPropertyMix(SchemaPropertyBase):
    def __init__(self, range_includes, default=None, many=False, *args, **kwargs):
        if not range_includes:
            raise ValueError("Missing value: range_includes can not be empty")
        for range_type in range_includes:
            if not isinstance(range_type, str) and not hasattr(range_type, "_meta"):
                raise ValueError(
                    "Invalid range value: Must be a schema class or a string name of a schema class - {range_type}"
                        .format(range_type=range_type))
        super().__init__(range_includes, default=default, many=many, *args, **kwargs)


########################################################################################################################


class Thing(Schema):
    name = TextProperty()
    identifications = TextProperty(many=True)

    class Meta:
        schema_class_name = "Thing"

    def __str__(self):
        return str(self.name)


class CreativeWork(Thing):
    year = IntegerProperty(default=1985)
    age = PositiveIntegerProperty()


class TVSeries(CreativeWork):
    series_description = TextProperty()


class TVSeason(CreativeWork):
    tv_series = ClassProperty(TVSeries)


class TVEpisode(CreativeWork):
    tv_series = ClassProperty("TVSeries")
    tv_season = ClassProperty(TVSeason)
    test = ClassPropertyMix([TVSeries, "TVSeason"])


work = CreativeWork(name="fffff")

json_data = {
    "instance_of": "TVSeason",
    "name": "Season 1",
    "age": 1,
    "tv_series": {
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
print(series1.tv_series.name)
print(series1.tv_series.age)
print(series1.tv_series.series_description)
series1.tv_series.name = "changed name"
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