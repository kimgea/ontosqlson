import inspect
import abc
from ontosqlson.meta import set_meta
from ontosqlson.property_base import SchemaPropertyBase, _register_property


class SchemaBase(abc.ABCMeta):

    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, SchemaBase)]
        if not parents:
            return super().__new__(cls, name, bases, attrs)

        meta_class = attrs.pop('Meta', None)  # Must pop Meta from attrs before sending it on
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        meta = meta_class or getattr(new_class, 'Meta', None)
        set_meta(new_class, meta, parents)

        _register_schema(new_class)
        _set_fields(new_class)

        _register_properties(new_class)
        _map_property_key_an_name(new_class)

        return new_class


def _register_schema(new_class):
    meta = new_class._meta
    meta.schema_collection.register_schema_model(meta.schema_class_name, meta.concrete_model)


def _register_properties(new_class):
    for key in new_class._meta.schema_fields:
        _register_property(getattr(new_class, key), key)


def _map_property_key_an_name(new_class):
    meta = new_class._meta
    for key in meta.schema_fields:
        property_name = getattr(new_class, key).property_name
        meta.property_name_attribute_name_lookup[property_name] = key
        meta.attribute_name_property_name_lookup[key] = property_name


def _set_fields(new_class):
    for attr in inspect.getmembers(new_class):
        key = attr[0]

        if key.startswith("__"):
            continue  # Skipp internal stuff
        if callable(getattr(new_class, key)):
            continue  # Skipp functions

        schema_field_or_empty = getattr(new_class._meta.concrete_model, key, {})
        is_schema_field = isinstance(schema_field_or_empty, SchemaPropertyBase)

        if is_schema_field:
            new_class._meta.schema_fields.append(key)
        else:
            new_class._meta.regular_attributes.append(key)
