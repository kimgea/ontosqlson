from weakref import WeakKeyDictionary
from ontosqlson.field.field_type_base import SchemaFieldTypeClass, SchemaFieldTypeBase


class SchemaFieldBase(object):
    def __init__(self, range_includes, field_name=None, default=None, many=False, *args, **kwargs):
        self.values = WeakKeyDictionary()

        self.field_name = field_name
        self._many = many
        self.default = default
        self.range_includes = range_includes

        self.range_includes = []
        self.range_includes_data_types = []
        self.range_includes_schema_types = []
        _set_range_includes(self, range_includes)

        _ensure_validate_default_value(self)

    def get_linked_schema_model(self, schema_name):
        for rage_obj in self.range_includes:
            range_is_schema = issubclass(type(rage_obj), SchemaFieldTypeClass)
            if range_is_schema and rage_obj.range_type._meta.schema_class_name == schema_name:
                return rage_obj.range_type
        return None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._many and instance not in self.values:
            self.values[instance] = []
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        if self._many:
            value = _ensure_validate_field_types(self, value)
        else:
            value = _ensure_validate_field_type(self, value)
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]


def _set_range_includes(field, range_includes):
    for i in range_includes:
        field.range_includes.append(i)
        if issubclass(type(i), SchemaFieldTypeClass):
            field.range_includes_schema_types.append(i)
        else:
            field.range_includes_data_types.append(i)


def _ensure_validate_default_value(field):
    if field.default is None:
        return

    field.default = _ensure_validate_field_type(field, field.default)


def _ensure_validate_field_types(field, values: list):
    for idx, value in enumerate(values):
        values[idx] = _ensure_validate_field_type(field, value)
    return values


def _ensure_validate_field_type(field, value):
    if any(ok_range.is_valid(value) for ok_range in field.range_includes):
        return value

    for ok_range in field.range_includes:
        fixed_value = ok_range.try_fix_value(value)
        if ok_range.is_valid(fixed_value):
            return fixed_value

    raise ValueError("Invalid field value: {field} can not be {value}"
                     .format(field=field.field_name, value=value))
