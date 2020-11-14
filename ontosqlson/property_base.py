from weakref import WeakKeyDictionary
import inspect
from ontosqlson.ontology import Ontology


class SchemaPropertyBase(object):
    def __init__(self, range_includes, property_name=None, default=None, many=False, *args, **kwargs):
        self.values = WeakKeyDictionary()
        self.schema_collection = Ontology()

        self.property_name = property_name
        self._many = many
        self.default = default

        self.range_includes = []
        self.range_includes_classes = []
        self.range_includes_class_names = []
        _set_range_includes(self, range_includes)

        _ensure_validate_default_value(self)

        if self.property_name:
            _register_property(self)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._many and instance not in self.values:
            self.values[instance] = []
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        if self._many:
            _ensure_validate_properties_types(self, value)
        else:
            _ensure_validate_property_type(self, value)
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]


def _set_range_includes(property, range_includes):
    for i in range_includes:
        property.range_includes.append(i)
        if hasattr(i, "_meta"):
            property.range_includes_classes.append(i)
            property.range_includes_class_names.append(i._meta.schema_class_name)
        else:
            property.range_includes_class_names.append(i)


def _set_property_name_if_not_set(property, property_name=None):
    if property.property_name is None:
        property.property_name = property_name


def _register_property(property, property_name=None):
    _set_property_name_if_not_set(property, property_name)

    if property.property_name is None and property_name is None:
        raise ValueError("self.property_name and property_name can not both be None")

    if property.property_name is not None:
        property.schema_collection.register_schema_property(property.property_name, property)


def _ensure_validate_default_value(property):
    if property.default is None:
        return

    _ensure_validate_property_type(property, property.default)


def _ensure_validate_properties_types(property, values: list):
    for value in values:
        _ensure_validate_property_type(property, value)


def _ensure_validate_property_type(property, value):
    # TODO: Refactor... wait until after property restructuring
    if hasattr(value, "_meta"):
        for ok_range in property.range_includes_class_names:
            if value._is_schema_type(ok_range):  # TODO: Look into refactor _is_schema_type
                return

        raise ValueError("Invalid property type: {value} not in {range_includes}".format(
            value=value._meta.schema_class_name, range_includes=property.range_includes_class_names))

    if isinstance(value, str) and str in property.range_includes:
        return
    if isinstance(value, int) and int in property.range_includes:
        return

    raise ValueError("Invalid property type: {value} not in {range_includes}".format(
        value=type(value), range_includes=property.range_includes_class_names))
