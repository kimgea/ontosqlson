import inspect
import abc
from entschema.schema.meta import set_meta
from entschema.field.field_base import SchemaFieldBase
from entschema.field.fields import TextField


class SchemaBase(abc.ABCMeta):

    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, SchemaBase)]
        if not parents:
            return super().__new__(cls, name, bases, attrs)

        meta_class = attrs.pop('Meta', None)  # Must pop Meta from attrs before sending it on
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        meta = meta_class or getattr(new_class, 'Meta', None)
        set_meta(new_class, meta, parents)

        _gather_attributes_and_fields(new_class)
        _try_set_field_names(new_class)
        _map_field_key_and_name(new_class)

        if not hasattr(new_class, new_class._meta.identification_field_name):
            setattr(new_class, new_class._meta.identification_field_name, TextField())

        return new_class


def _try_set_field_names(new_class):
    for key in new_class._meta.schema_fields:
        field = getattr(new_class, key)
        if field.field_name is None:
            field.field_name = key


def _map_field_key_and_name(new_class):
    meta = new_class._meta
    for key in meta.schema_fields:
        field_name = getattr(new_class, key).field_name
        meta.field_attribute_name_map[field_name] = key
        meta.attribute_field_name_map[key] = field_name


def _gather_attributes_and_fields(new_class):
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
