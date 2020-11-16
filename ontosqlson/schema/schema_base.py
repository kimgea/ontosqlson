import inspect
import abc
from ontosqlson.schema.meta import set_meta
from ontosqlson.field.field_base import SchemaFieldBase


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

        _register_fields(new_class)
        _map_field_key_and_name(new_class)

        return new_class


def _register_schema(new_class):
    meta = new_class._meta
    meta.schema_collection.register_schema_model(meta.schema_class_name, meta.concrete_model)


def _register_fields(new_class):
    for key in new_class._meta.schema_fields:
        _register_field(getattr(new_class, key), key)


def _register_field(field, field_name=None):
    if field.field_name is not None:
        return
    field.field_name = field_name
    field.schema_collection.register_schema_fields(field.field_name, field)


def _map_field_key_and_name(new_class):
    meta = new_class._meta
    for key in meta.schema_fields:
        field_name = getattr(new_class, key).field_name
        meta.field_attribute_name_map[field_name] = key
        meta.attribute_field_name_map[key] = field_name


def _set_fields(new_class):
    for attr in inspect.getmembers(new_class):
        key = attr[0]

        if key.startswith("__"):
            continue  # Skipp internal stuff
        if callable(getattr(new_class, key)):
            continue  # Skipp functions

        schema_field_or_empty = getattr(new_class._meta.concrete_model, key, {})
        is_schema_field = isinstance(schema_field_or_empty, SchemaFieldBase)

        if is_schema_field:
            new_class._meta.schema_fields.append(key)
        else:
            new_class._meta.regular_attributes.append(key)
